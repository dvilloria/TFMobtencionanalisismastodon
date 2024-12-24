import psycopg2
import networkx as nx
import requests
from mastodon import Mastodon, MastodonNetworkError, MastodonVersionError
import matplotlib.pyplot as plt
import pandas as pd
# Datos conexión bd
Config_bd = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '0512',
    'host': 'localhost',
    'port': 5432
}

def obtener_vecinos(instancia):
    try:
        #print(f'Conectando a: https://{instancia}')
        mastodon = Mastodon(api_base_url=f'https://{instancia}')
        vecinos = mastodon.instance_peers()
        #print(f'tiene {len(vecinos)} vecinos la instancia {instancia}')
        return vecinos
    except (MastodonNetworkError, MastodonVersionError) as e:
        print(f"Error con la instancia {instancia}: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado con {instancia}: {e}")
        return []

def table_activas():
    try: 
        conex = psycopg2.connect(**Config_bd)
        cursor = conex.cursor()
        cursor.execute("""
            CREATE TABLE instancias_reales AS
            SELECT instancia, num_vecinos
            FROM instancias_final
            WHERE num_vecinos > 0;
        """)
        conex.commit()
        cursor.close()
        conex.close()
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

table_activas()

Grafo_activas = nx.DiGraph()

def creacion_grafo_act():
    try: 
        conex = psycopg2.connect(**Config_bd)
        cursor = conex.cursor()
        cursor.execute("""
            SELECT instancia FROM instancias_reales
        """)
        activas = [row[0] for row in cursor.fetchall()]
        i = 0
        for activa in activas:
            vecinos = obtener_vecinos(activa)
            vecinos_act = [vecino for vecino in vecinos if vecino in activas]
            for vecino_act in vecinos_act:
                Grafo_activas.add_edge(activa, vecino_act)
            #print(f"Procesada {activa}: {len(vecinos_act)} vecinos añadidos al grafo.")
            print(i)
            i = i + 1
        conex.commit()
        cursor.close()
        conex.close()
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

creacion_grafo_act()

# Guardar el grafo como archivo
nx.write_gml(Grafo_activas, "grafo_activas.gml")  #formato GML
print("Grafo guardado en grafo_activas.gml.")
