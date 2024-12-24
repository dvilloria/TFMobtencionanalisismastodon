# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:21:37 2024

@author: villo
"""
# Importación de las librerias
from mastodon import Mastodon, MastodonNetworkError, MastodonVersionError
import time
from dotenv import load_dotenv
import os 
import random
import requests 
import json
import networkx as nx
import psycopg2
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

# Función para ver si una instancia está activa y obtener sus vecinos
def obtener_vecinos(instancia):
    try:
        print(f'Conectando a: https://{instancia}')
        mastodon = Mastodon(api_base_url=f'https://{instancia}')
        vecinos = mastodon.instance_peers()
        print(f'tiene {len(vecinos)} vecinos la instancia {instancia}')
        return vecinos
    except (MastodonNetworkError, MastodonVersionError) as e:
        print(f"Error con la instancia {instancia}: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado con {instancia}: {e}")
        return []
    
    
# Configuración postgreSQL

Config_bd = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '0512',
    'host': 'localhost',
    'port': 5432
}

# Lista visitadas
instancias_visitadas = set()
visitadas_lock = threading.Lock()
# cola instancias
cola_instancias = Queue()
cola_instancias.put('mastodon.social')
# Intancias activas
instancias_activas = []
# Semáforo
contador_tareas = threading.Semaphore(1)

def guardar_bd(instancia, num_veci):
    try: 
        conex = psycopg2.connect(**Config_bd)
        cursor = conex.cursor()
        cursor.execute("""
            INSERT INTO instancias (instancia, num_vecinos)
            VALUES (%s, %s)
            ON CONFLICT (instancia) DO NOTHING;
        """, (instancia, num_veci))
        conex.commit()
        cursor.close()
        conex.close()
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        
        
def procesar_instancia(instancia_actual):
    global instancias_visitadas
    with visitadas_lock:
        if instancia_actual in instancias_visitadas:
            return
        instancias_visitadas.add(instancia_actual)

    # Obtener vecinos de la instancia actual
    vecinos = obtener_vecinos(instancia_actual)  
    num_veci = len(vecinos)
    print(f"Procesando instancia: {instancia_actual}, vecinos: {num_veci}")
    guardar_bd(instancia_actual, num_veci)
    if num_veci > 0:
        instancias_activas.append(instancia_actual)
    for vecino in vecinos:
        with visitadas_lock:
            if vecino not in instancias_visitadas:
                cola_instancias.put(vecino)
                contador_tareas.release()
                
    contador_tareas.acquire()
              
    
# Ejecutar el pool de hilos
with ThreadPoolExecutor(max_workers=10) as executor:
    while True:
        try:
            instancia = cola_instancias.get(timeout=10)  # Esperar nueva instancia
            contador_tareas.release()  # Contar la tarea como activa
            executor.submit(procesar_instancia, instancia)
        except Exception:
            break  # Salir si no hay más tareas en la cola por un tiempo    
    

# Configuración del pool de hilos
#with ThreadPoolExecutor(max_workers=10) as executor:  # Ajusta el número de trabajadores según tu hardware
#    while not cola_instancias.empty():
#        instancia = cola_instancias.get()
#        executor.submit(procesar_instancia, instancia)

print(f"\nInstancias activas encontradas: {len(instancias_visitadas)}")        
        
