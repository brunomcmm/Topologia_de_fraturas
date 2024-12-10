"""
analysis.py

Módulo para análise topológica das interseções entre fraturas.
Classifica os tipos de nós (X, Y, I) com base na proximidade e no número de conexões.
"""

from collections import Counter
from scipy.spatial import KDTree

def analyze_intersections(intersections, radius):
    """
    Analisa as interseções entre fraturas e classifica os nós em X, Y e I.

    Args:
        intersections (list): Lista de coordenadas das interseções (x, y).
        radius (int): Raio para agrupar interseções próximas como o mesmo nó.

    Returns:
        dict: Contagem dos tipos de nós (X, Y, I).
    """
    if not intersections:
        return {"X-nodes": 0, "Y-nodes": 0, "I-nodes": 0}

    # Criar um KDTree para encontrar interseções próximas
    tree = KDTree(intersections)
    groups = tree.query_ball_tree(tree, radius)

    # Agrupar interseções próximas como nós únicos
    unique_nodes = [tuple(map(int, map(round, tree.data[group].mean(axis=0)))) for group in groups]
    unique_nodes = list(set(unique_nodes))  # Remover duplicatas

    # Contar conexões para cada nó
    connection_counts = Counter()
    for group in groups:
        connection_counts[len(group)] += 1

    # Classificar nós com base no número de conexões
    node_counts = {
        "X-nodes": connection_counts[4],  # 4 conexões (cruzamentos em X)
        "Y-nodes": connection_counts[3],  # 3 conexões (junções em Y)
        "I-nodes": connection_counts[1],  # 1 conexão (extremidades isoladas)
    }

    return node_counts