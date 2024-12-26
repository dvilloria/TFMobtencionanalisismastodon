from igraph import Graph, plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr
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

