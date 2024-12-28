# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 18:30:09 2024

@author: villo
"""

from igraph import Graph, plot

# Leer el grafo desde el archivo GML
grafo = Graph.Read_GML("C:/Users/villo/OneDrive/Desktop/grafo_activas.gml")

# Calcular coreness y asignar colores
coreness = grafo.coreness()
umbral = 1000
colores = ['#FF5733' if c >= umbral else '#3498DB' for c in coreness]

# Generar layout para el grafo
layout = grafo.layout_kamada_kawai(epsilon=1e-5)

visual_style = {
    "vertex_size": 15,  # Tamaño de los nodos
    "vertex_color": colores,  # Color de los nodos
    "edge_width": 0.5,  # Grosor de las aristas
    "layout": layout,  # Layout del grafo
    "bbox": (800, 800),  # Tamaño de la figura
    "margin": 20,  # Margen alrededor del grafo
    "vertex_label": None,  # Sin etiquetas para los nodos
}

plot(grafo, "grafo_core_periferia3.png", **visual_style)
print("Grafo guardado como 'grafo_core_periferia3.png'")