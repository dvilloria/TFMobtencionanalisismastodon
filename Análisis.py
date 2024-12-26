from igraph import Graph, plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr
from igraph import VertexDendrogram
# Carga del grafo
grafo = Graph.Read_GML("grafo_activas.gml")
# Info básica
print("Número de nodos:", grafo.vcount())
print("Número de aristas:", grafo.ecount())
print("¿Es dirigido?:", grafo.is_directed())
# Densidad
densidad = grafo.density()
print("Densidad del grafo:", densidad)
grados_salida = grafo.degree(mode="out")  # Grado de salida
grados_entrada = grafo.degree(mode="in")  # Grado de entrada
# Relación entre grados de salida y de entrada
pearson_corr, _ = pearsonr(grados_entrada, grados_salida)
spearman_corr, _ = spearmanr(grados_entrada, grados_salida)
print(f"Correlación de Pearson: {pearson_corr:.3f}")
print(f"Correlación de Spearman: {spearman_corr:.3f}")
## Scatterplot grados salida/entrada
plt.figure(figsize=(8, 6))
plt.scatter(grados_salida, grados_entrada, alpha=0.6, edgecolor='k')
plt.title("Scatterplot de grados de entrada vs grados de salida")
plt.xlabel("Grado de salida")
plt.ylabel("Grado de entrada")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('Scatterplot grados entrada y salida')
plt.show()
## Distribución grados de entrada y salida
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].hist(grados_entrada, bins=50, color='blue', alpha=0.7)
ax[0].set_title('Histograma de Grados de Entrada')
ax[0].set_xlabel('Grado de Entrada')
ax[0].set_ylabel('Frecuencia')
ax[1].hist(grados_salida, bins=50, color='green', alpha=0.7)
ax[1].set_title('Histograma de Grados de Salida')
ax[1].set_xlabel('Grado de Salida')
ax[1].set_ylabel('Frecuencia')
plt.tight_layout()
plt.savefig('Distribución grados entrada y salida')
plt.show()
# Métricas sobre grados de salida
media = np.mean(grados_salida)
mediana = np.median(grados_salida)
varianza = np.var(grados_salida)
print(f"Media: {media}, Mediana: {mediana}, Varianza: {varianza}")
# Métricas sobre grados de entrada
media = np.mean(grados_entrada)
mediana = np.median(grados_entrada)
varianza = np.var(grados_entrada)
print(f"Media: {media}, Mediana: {mediana}, Varianza: {varianza}")
# top 10 instancias con mayor grado de entrada
top_entrada = sorted(zip(range(len(grados_entrada)), grados_entrada), key=lambda x: x[1], reverse=True)[:10]
# top 10 instancias con mayor grado de salida
top_salida = sorted(zip(range(len(grados_salida)), grados_salida), key=lambda x: x[1], reverse=True)[:10]
# Nombres
top_entrada_nombres = [(grafo.vs["label"][node], grado) for node, grado in top_entrada]
top_salida_nombres = [(grafo.vs["label"][node], grado) for node, grado in top_salida]
print("Top 10 nodos con mayor grado de entrada (nombres):", top_entrada_nombres)
print("Top 10 nodos con mayor grado de salida (nombres):", top_salida_nombres)
# Componentes débilmente conexas
debil_conexas = grafo.connected_components(mode="weak")
num_debil_conexas = len(debil_conexas)
tam_debil_max = max(debil_conexas.sizes())
# Componentes fuertemente conexas
fuerte_conexas = grafo.connected_components(mode="strong")
num_fuerte_conexas = len(fuerte_conexas)
tam_fuerte_max = max(fuerte_conexas.sizes())
print("\nComponentes conexas:")
print(f"Número de componentes débilmente conexas: {num_debil_conexas}")
print(f"Tamaño de la componente débilmente conexa más grande: {tam_debil_max}")
print(f"Número de componentes fuertemente conexas: {num_fuerte_conexas}")
print(f"Tamaño de la componente fuertemente conexa más grande: {tam_fuerte_max}")
print(set(fuerte_conexas.sizes()))
# Centralidad de grado
centralidad_grado = grafo.degree(mode="all")
top_centralidad_grado = sorted(zip(range(len(centralidad_grado)), centralidad_grado), key=lambda x: x[1], reverse=True)[:10]
# Centralidad de cercanía
centralidad_cercania = grafo.closeness(mode="all")
top_centralidad_cercania = sorted(zip(range(len(centralidad_cercania)), centralidad_cercania), key=lambda x: x[1], reverse=True)[:10]
# Centralidad de intermediación
centralidad_intermediacion = grafo.betweenness()
top_centralidad_intermediacion = sorted(zip(range(len(centralidad_intermediacion)), centralidad_intermediacion), key=lambda x: x[1], reverse=True)[:10]
print("\nMétricas de centralidad:")
top_grados_nombres = [(grafo.vs["label"][node], grado) for node, grado in top_centralidad_grado]
top_cercania_nombres = [(grafo.vs["label"][node], grado) for node, grado in top_centralidad_cercania]
top_intermediacion_nombres = [(grafo.vs["label"][node], grado) for node, grado in top_centralidad_intermediacion]
print("Top 10 nodos con mayor grado conjunto (nombres):", top_grados_nombres)
print("Top 10 nodos con mayor cercanía (nombres):", top_cercania_nombres)
print("Top 10 nodos con mayor intermediación (nombres):", top_intermediacion_nombres)
n = len(grafo.vs)
centralidad_intermediacion_norm = [ b / ((n-1)*(n-2)) for b in centralidad_intermediacion]
top_centralidad_intermediacion_norm = sorted(zip(range(len(centralidad_intermediacion_norm)), centralidad_intermediacion_norm), 
                                             key=lambda x: x[1], reverse=True)[:10]
top_intermediacion_nombres_norm = [(grafo.vs["label"][node], grado) for node, grado in top_centralidad_intermediacion_norm]
print("Top 10 nodos con mayor intermediación (nombres):", top_intermediacion_nombres_norm)
# Media y desviación estándar de centralidad de grado
media_grado = np.mean(centralidad_grado)
desviacion_grado = np.std(centralidad_grado)
# Media y desviación estándar de centralidad de cercanía
media_cercania = np.mean(centralidad_cercania)
desviacion_cercania = np.std(centralidad_cercania)
# Media y desviación estándar de centralidad de intermediación
media_intermediacion = np.mean(centralidad_intermediacion)
desviacion_intermediacion = np.std(centralidad_intermediacion)
media_intermediacion_norm = np.mean(centralidad_intermediacion_norm)
desviacion_intermediacion_norm = np.std(centralidad_intermediacion_norm)
# Imprimir resultados
print("\nEstadísticas de las métricas de centralidad:")
print(f"Centralidad de grado - Media: {media_grado:.2f}, Desviación estándar: {desviacion_grado:.2f}")
print(f"Centralidad de cercanía - Media: {media_cercania:.2f}, Desviación estándar: {desviacion_cercania:.2f}")
print(f"Centralidad de intermediación - Media: {media_intermediacion:.2f}, Desviación estándar: {desviacion_intermediacion:.2f}")
print(f"Centralidad de intermediación normalizada - Media: {media_intermediacion_norm:.4f}, Desviación estándar: {desviacion_intermediacion_norm:.4f}")
# Distribución grado conjunto y cercanía
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].hist(centralidad_grado, bins=50, color='blue', alpha=0.7)
ax[0].set_title('Histograma de grados conjuntos')
ax[0].set_xlabel('Grado')
ax[0].set_ylabel('Frecuencia')
ax[1].hist(centralidad_cercania, bins=50, color='green', alpha=0.7)
ax[1].set_title('Histograma de centralidad cercanía')
ax[1].set_xlabel('Cercanía')
ax[1].set_ylabel('Frecuencia')
plt.tight_layout()
plt.savefig('Distribución Cercanía y grado')
plt.show()
# Distribución de la intermediación
valores_unicos, frecuencias = np.unique(centralidad_intermediacion, return_counts=True)
plt.figure(figsize=(6, 4))
plt.loglog(valores_unicos, frecuencias, marker=".", linestyle="none")
plt.xlabel('Intermediación')
plt.ylabel('Frecuencia')
plt.title('Distribución de la intermediación (Log-Log)')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.savefig('Distribución intermediación (Log-Log')
plt.show()
# Caminos y diámetro
promedio_caminos = grafo.average_path_length()
diametro = grafo.diameter()
print("\nConectividad del grafo:")
print(f"Promedio de longitud de caminos: {promedio_caminos}")
print(f"Diámetro del grafo: {diametro}")
grafo.to_undirected()
# Detección de comunidades
# Louvain
comunidades = grafo.community_multilevel()
num_comunidades = len(comunidades)
print(f"\nDetección de comunidades:")
print(f"Número de comunidades detectadas: {num_comunidades}")
print(f"Tamaños de las comunidades: {comunidades.sizes()}")
# Calcular la modularidad de esta partición
modularidad = grafo.modularity(comunidades)
print(f"Modularidad de las comunidades detectadas por Louvain: {modularidad}")
# Fast greedy
comunidades2 = grafo.community_fastgreedy()
# Convertir el dendrograma en la partición de comunidades
comunidades_fastgreedy_partition = comunidades2.as_clustering()
num_comunidades = len(comunidades_fastgreedy_partition)
# Calcular la modularidad de esta partición
modularidad = grafo.modularity(comunidades_fastgreedy_partition)
print(f"Modularidad de las comunidades detectadas por FastGreedy: {modularidad}")
print(f"\nDetección de comunidades:")
print(f"Número de comunidades detectadas: {num_comunidades}")
print(f"Tamaños de las comunidades: {comunidades_fastgreedy_partition.sizes()}")
# Carga otra vez del grafo para que sea dirigido
grafo2 = Graph.Read_GML("grafo_activas.gml")
print("Número de nodos:", grafo2.vcount())
print("Número de aristas:", grafo2.ecount())
print("¿Es dirigido?:", grafo2.is_directed())
# Coeficiente de clustering global
coeficiente_clustering_global = grafo2.transitivity_undirected() 
print(f"Coeficiente de clustering global: {coeficiente_clustering_global}")
# coeficiente de clustering local para cada nodo
coeficientes_locales = grafo.transitivity_local_undirected()
# Ordenar los coeficientes de clustering locales en orden descendente
nodos_top_clustering = sorted(enumerate(coeficientes_locales), key=lambda x: x[1], reverse=True)[:10]
# Mostrar los 10 nodos con el coeficiente de clustering local más alto y sus nombres
print("Top 10 nodos con mayor coeficiente de clustering local:")
for nodo, coef in nodos_top_clustering:
    print(f"Nodo {grafo.vs['label'][nodo]} tiene un coeficiente de clustering local de {coef}")
# Distribución del coeficiente clustering
plt.hist(coeficientes_locales, bins=50)
plt.title("Distribución del coeficiente de clustering")
plt.xlabel("Coeficiente clustering")
plt.ylabel("Frecuencia")
plt.savefig('Distribución del coeficiente clustering')
plt.show()
