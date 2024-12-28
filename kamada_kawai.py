# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:12:39 2024

@author: villo
"""

from igraph import Graph, plot
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
grafo = Graph.Read_GML("C:/Users/villo/OneDrive/Desktop/grafo_activas.gml")
degree = grafo.degree()
intermediacion = grafo.betweenness()
print('Intermediación finalizada')
max_degree = max(degree)
#max_betweenness = max(intermediacion)
sizes = [10 + (d / max_degree) * 50 for d in degree]
#colors = [(b / max_betweenness) for b in intermediacion]
layout = grafo.layout_kamada_kawai(epsilon=1e-3)
colores = [to_hex(plt.cm.plasma(c)) for c in intermediacion]

visual_style = {
    "vertex_size": sizes,  # Tamaño de los nodos
    "vertex_color": colores,  # Color de los nodos
    "edge_width": 0.5,  # Grosor de las aristas
    "layout": layout,  # Layout del grafo
    "bbox": (800, 800),  # Tamaño de la figura
    "margin": 20,  # Margen alrededor del grafo
    "vertex_label": None,  # Sin etiquetas para los nodos
}

# Guardar el gráfico
plot(grafo, "grafo_kamada.png", **visual_style)

print("Grafo guardado como 'grafo_denso_colores.png'")