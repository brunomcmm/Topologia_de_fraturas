"""
intersection_utils.py

Módulo para encontrar interseções entre linhas detectadas em imagens.
Inclui cálculos matemáticos necessários para determinar os pontos de interseção.
"""

def calculate_intersection(line1, line2):
    """
    Calcula a interseção entre duas linhas.

    Args:
        line1 (tuple): Coordenadas da primeira linha (x1, y1, x2, y2).
        line2 (tuple): Coordenadas da segunda linha (x3, y3, x4, y4).

    Returns:
        tuple: Coordenadas da interseção (x, y) ou None se não houver interseção.
    """
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Linhas paralelas ou coincidentes

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    if (
        min(x1, x2) <= px <= max(x1, x2)
        and min(y1, y2) <= py <= max(y1, y2)
        and min(x3, x4) <= px <= max(x3, x4)
        and min(y3, y4) <= py <= max(y3, y4)
    ):
        return (int(px), int(py))
    return None

def find_intersections(lines):
    """
    Encontra as interseções entre as linhas detectadas.

    Args:
        lines (list): Lista de linhas detectadas (coordenadas x1, y1, x2, y2).

    Returns:
        list: Coordenadas das interseções (x, y).
    """
    intersections = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            intersection = calculate_intersection(lines[i][0], lines[j][0])
            if intersection:
                intersections.append(intersection)
    return intersections