#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import networkx as nx
import requests
from mastodon import Mastodon, MastodonNetworkError, MastodonVersionError
import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


# Datos conexión bd
Config_bd = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '0512',
    'host': 'localhost',
    'port': 5432
}


# In[3]:


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


# In[4]:


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


# In[5]:


table_activas()


# In[6]:


Grafo_activas = nx.DiGraph()


# In[7]:


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


# In[8]:


creacion_grafo_act()


# In[ ]:


# Guardar el grafo como archivo (opcional)
nx.write_gml(Grafo_activas, "grafo_activas.gml")  # Guarda en formato GML
print("Grafo guardado en grafo_activas.gml.")


# In[ ]:


grafo = nx.read_gml('grafo_activas.gml')


# In[ ]:


# Acceder a nodos y aristas
print("Nodos:", len(grafo.nodes()))
print("Aristas:", len(grafo.edges()))


# In[ ]:


47895443/(12409*12408)


# In[ ]:


nx.density(grafo)


# In[ ]:


import numpy as np


# In[ ]:


# Como es un  grafo dirigido veamos los grados de entrada y salida.
grado_entrada = [grado for _, grado in grafo.in_degree()]
grado_salida = [grado for _, grado in grafo.out_degree()]


# In[ ]:


print(f"Grado promedio de entrada: {np.mean(grado_entrada)}")
print(f"Grado promedio de salida: {np.mean(grado_salida)}")


# In[ ]:


grafo.is_directed()


# In[ ]:


import matplotlib.pyplot as plt

# Dibuja el grafo
pos = nx.spring_layout(grafo)
plt.figure(figsize=(10, 10))
nx.draw(grafo, pos, node_size=20, edge_color='gray', with_labels=False)
plt.title("Visualización del Grafo")
plt.show()


# In[ ]:


# Distribución de grados
plt.hist(grado_entrada, bins=50, alpha=0.7, label='Grado de entrada')
plt.xlabel('Grado de entrada')
plt.ylabel('Frecuencia')
plt.legend()
plt.title('Distribución de Grados de entrada')
plt.savefig('Distribución grados entrada')
plt.show()


# In[ ]:


plt.hist(grado_salida, bins=50, alpha=0.7, label='Grado de salida')
plt.xlabel('Grado salida')
plt.ylabel('Frecuencia')
plt.legend()
plt.title('Distribución de Grados de salida')
plt.savefig('Distribución grados salida')
plt.show()


# In[ ]:


valores_unicos, frecuencias = np.unique(grado_entrada, return_counts=True)
plt.figure(figsize=(6, 4))
plt.loglog(valores_unicos, frecuencias, marker=".", linestyle="none")
plt.xlabel('Grado')
plt.ylabel('Frecuencia')
plt.title('Distribución de grados de entrada (Log-Log')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.savefig('Distribución grados entrada (Log-Log')
plt.show()


# In[ ]:


valores_unicos, frecuencias = np.unique(grado_salida, return_counts=True)
plt.figure(figsize=(6, 4))
plt.loglog(valores_unicos, frecuencias, marker=".", linestyle="none")
plt.xlabel('Grado')
plt.ylabel('Frecuencia')
plt.title('Distribución de grados de salida (Log-Log')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.savefig('Distribución grados salida (Log-Log')
plt.show()


# In[ ]:


# Grado de entrada (in-degree)
grado_entrada = grafo.in_degree()
nodos_mayor_grado_entrada = sorted(grado_entrada, key=lambda x: -x[1])[:5]
print("Top 5 nodos con mayor grado de entrada:", nodos_mayor_grado_entrada)

# Grado de salida (out-degree)
grado_salida = grafo.out_degree()
nodos_mayor_grado_salida = sorted(grado_salida, key=lambda x: -x[1])[:5]
print("Top 5 nodos con mayor grado de salida:", nodos_mayor_grado_salida)

# Grado total (in-degree + out-degree)
grado_total = grafo.degree()
nodos_mayor_grado_total = sorted(grado_total, key=lambda x: -x[1])[:5]
print("Top 5 nodos con mayor grado total:", nodos_mayor_grado_total)


# In[ ]:


# Componentes debilmente conexas
num_componentes = len(list(nx.weakly_connected_components(grafo)))
print("Número de componentes débilmente conexas:", num_componentes)


# In[ ]:


# Componentes fuertemente conexas
num_componentes = len(list(nx.strongly_connected_components(grafo)))
print("Número de componentes fuertemente conexas:", num_componentes)


# In[ ]:


# Obtener las componentes fuertemente conexas
componentes_fuertes = list(nx.strongly_connected_components(grafo))

# Calcular el tamaño de cada componente
tamaños = [len(componente) for componente in componentes_fuertes]

# Mostrar los tamaños
for i, tam in enumerate(tamaños, start=1):
    if tam > 1:
        print(f"Componente {i}: Tamaño {tam}")


# In[ ]:


# Asortatividad
asortatividad = nx.degree_assortativity_coefficient(grafo)
print("Coeficiente de asortatividad:", asortatividad)


# In[ ]:


# Subgrafo fuertemente conexo
subcentral = grafo.subgraph(max(componentes_fuertes, key=len)).copy()
grafo_no_dirigido = grafo.to_undirected()


# Caminos más cortos y diámetro
# Longitud promedio del camino más corto
longitud_media = nx.average_shortest_path_length(subcentral)
print("Longitud promedio del camino más corto:", longitud_media)

# Diámetro del grafo
diametro = nx.diameter(subcentral)
print("Diámetro del grafo:", diametro)

# Caminos más cortos y diámetro
# Longitud promedio del camino más corto
longitud_media = nx.average_shortest_path_length(grafo_no_dirigido)
print("Longitud promedio del camino más corto:", longitud_media)

# Diámetro del grafo
diametro = nx.diameter(grafo_no_dirigido)
print("Diámetro del grafo:", diametro)


# In[ ]:


# Centralidad de grado
centralidad_grado = nx.degree_centrality(grafo)
print("Centralidad de grado (top 5):", sorted(centralidad_grado.items(), key=lambda x: -x[1])[:5])

# Centralidad de intermediación
centralidad_intermediacion = nx.betweenness_centrality(grafo)
print("Centralidad de intermediación (top 5):", sorted(centralidad_intermediacion.items(), key=lambda x: -x[1])[:5])

# Centralidad de cercanía
centralidad_cercania = nx.closeness_centrality(grafo)
print("Centralidad de cercanía (top 5):", sorted(centralidad_cercania.items(), key=lambda x: -x[1])[:5])


# In[ ]:


# Detección de comunidades con el algoritmo Louvain
from networkx.algorithms.community import greedy_modularity_communities

comunidades = list(greedy_modularity_communities(grafo))
print("Número de comunidades detectadas:", len(comunidades))
print("Tamaños de las comunidades (top 5):", [len(c) for c in comunidades[:5]])


# In[ ]:


# Simula eliminación de nodos
import random

# Elimina nodos aleatorios y mide impacto
nodos_a_eliminar = random.sample(list(grafo.nodes()), 10)  # 10 nodos aleatorios
grafo_copia = grafo.copy()
grafo_copia.remove_nodes_from(nodos_a_eliminar)

# Calcula tamaño de la componente gigante después de eliminar nodos
componentes = sorted(nx.strongly_connected_components(grafo_copia), key=len, reverse=True)
print("Tamaño de la componente gigante tras eliminación:", len(componentes[0]) if componentes else 0)

