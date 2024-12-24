# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import random
import psycopg2
from psycopg2.extras import execute_values
from mastodon import Mastodon

Config_bd = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '0512',
    'host': 'localhost',
    'port': 5432
}

# Conexión a la base de datos
conn = psycopg2.connect(**Config_bd)
cursor = conn.cursor()
# Crear tabla
def crear_tabla():
    try:
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS instancias_final (
                       instancia VARCHAR(255) PRIMARY KEY,
                       num_vecinos INTEGER,
                       estado VARCHAR(50) DEFAULT 'no_comprobada',
                       fecha_agregada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       fecha_comprobada TIMESTAMP
                       );""")
        conn.commit()
        print("Tabla 'instancias_final' creada o ya existente.")
    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")
        conn.rollback()        

def insertar_instancia_inicial(instancia):
    try:
        cursor.execute("""
            INSERT INTO instancias_final (instancia, estado, num_vecinos)
            VALUES (%s, %s, %s)
            ON CONFLICT (instancia) DO NOTHING;
        """, (instancia, 'no_comprobada', 0))
        conn.commit()
        print(f"Instancia inicial '{instancia}' añadida.")
    except psycopg2.Error as e:
        print(f"Error al insertar instancia inicial: {e}")
        conn.rollback()

def obtener_instancia_no_comprobada():
    try:
        cursor.execute("SELECT instancia FROM instancias_final WHERE estado = 'no_comprobada' ORDER BY RANDOM() LIMIT 1;")
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Error al obtener instancia: {e}")
        conn.rollback()  # Revertir transacción fallida
        return None
    
def actualizar_estado_instancia(id_instancia, estado):
    cursor.execute("UPDATE instancias_final SET estado = %s, fecha_comprobada = CURRENT_TIMESTAMP WHERE instancia = %s;", (estado, id_instancia))
    conn.commit()
    
    
def agregar_vecinos(vecinos):
    cursor.execute("SELECT instancia FROM instancias_final;")
    existentes = set(row[0] for row in cursor.fetchall())
    
    vecinos_filtrados = [vecino for vecino in vecinos if not vecino.endswith('activitypub-troll.cf')]
    
    nuevos = [(vecino, 'no_comprobada', None) for vecino in vecinos_filtrados if vecino not in existentes]
    if nuevos:
        execute_values(cursor, """
            INSERT INTO instancias_final (instancia, estado, num_vecinos) VALUES %s;
        """, nuevos)
        conn.commit()
        
        
def obtener_vecinos(instancia):
    try:
        mastodon = Mastodon(api_base_url=f'https://{instancia}')
        vecinos = mastodon.instance_peers()
        return vecinos
    except Exception as e:
        print(f"Error al obtener vecinos de {instancia}: {e}")
        return []
    
def actualizar_num_vecinos(id_instancia, num_vecinos):
    try:
        cursor.execute("UPDATE instancias_final SET num_vecinos = %s WHERE instancia = %s;", (num_vecinos, id_instancia))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error al actualizar num_vecinos: {e}")
        conn.rollback()
        
crear_tabla()

insertar_instancia_inicial('mastodon.social')

        
# Bucle principal
while True: 
    instancia = obtener_instancia_no_comprobada()
    if not instancia:
        print("Todas las instancias están comprobadas.")
        break
    
    nombre_instancia = instancia[0]
    print(f"Comprobando la instancia: {nombre_instancia}")

    # Marcar como "comprobando"
    actualizar_estado_instancia(nombre_instancia, 'comprobando')

    # Obtener vecinos y agregarlos a la base de datos
    vecinos = obtener_vecinos(nombre_instancia)
    num_vecinos = len(vecinos)
    agregar_vecinos(vecinos)
    actualizar_num_vecinos(nombre_instancia, num_vecinos)

    # Marcar como "comprobada"
    actualizar_estado_instancia(nombre_instancia, 'comprobada')

print("Proceso completado.")
cursor.close()
conn.close()
