# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 19:58:54 2024

@author: villo
"""

from igraph import Graph, plot
grafo = Graph.Read_GML("C:/Users/villo/OneDrive/Desktop/grafo_activas.gml")
coreness = grafo.coreness()
umbral = 1000
colores = ['#FF5733' if c >= umbral else '#3498DB' for c in coreness]
layout = grafo.layout_fruchterman_reingold(niter=500)
visual_style = {
    "vertex_size": 20,  # Tamaño de los nodos
    "vertex_color": colores,  # Colores según núcleo o periferia
    "edge_width": 0.5,  # Grosor de las aristas
    "layout": layout,  # Layout del grafo
    "bbox": (800, 800),  # Tamaño de la figura
    "margin": 20,  # Margen alrededor del grafo
    "vertex_label": None,  # Sin etiquetas
}
plot(grafo, "grafo_core_periferia.png", **visual_style)
print("Grafo guardado como 'grafo_core_periferia.png'")
