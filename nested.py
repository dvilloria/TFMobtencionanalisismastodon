# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 20:05:46 2024

@author: villo
"""

from igraph import Graph
import numpy as np

g = Graph.Read_GML("C:/Users/villo/OneDrive/Desktop/grafo_activas.gml")
adj_matrix = np.array(g.get_adjacency().data)

# Calcular el índice NODF (nestedness)
def calculate_nodf(matrix):
    """
    Calcula el índice de nestedness (NODF) de una matriz binaria de adyacencia.
    """
    rows, cols = matrix.shape
    nestedness = 0

    # Normalizar matriz a binaria (0s y 1s)
    matrix = (matrix > 0).astype(int)

    # Comparación fila a fila
    for i in range(rows):
        for j in range(i + 1, rows):
            overlap = np.sum(np.logical_and(matrix[i, :], matrix[j, :]))
            min_degree = min(np.sum(matrix[i, :]), np.sum(matrix[j, :]))
            if min_degree > 0:
                nestedness += overlap / min_degree

    # Comparación columna a columna
    for i in range(cols):
        for j in range(i + 1, cols):
            overlap = np.sum(np.logical_and(matrix[:, i], matrix[:, j]))
            min_degree = min(np.sum(matrix[:, i]), np.sum(matrix[:, j]))
            if min_degree > 0:
                nestedness += overlap / min_degree

    # Normalizar por el número total de comparaciones
    total_pairs = (rows * (rows - 1) / 2) + (cols * (cols - 1) / 2)
    return nestedness / total_pairs


nodf_value = calculate_nodf(adj_matrix)
print(f"NODF (Nestedness): {nodf_value}")