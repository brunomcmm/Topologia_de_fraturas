"""
image_processing.py

Módulo para processar imagens e identificar fraturas e interseções.
Inclui funções para converter a imagem em escala de cinza, detectar fraturas (linhas),
categorizar interseções (nós), e gerar uma imagem com as fraturas destacadas para o preview.
"""

import cv2
import numpy as np
from analysis import analyze_intersections

def process_image(image_path, sensitivity, intersection_radius):
    """
    Processa a imagem para identificar fraturas e realizar análise topológica.

    Args:
        image_path (str): Caminho para a imagem.
        sensitivity (int): Sensibilidade para detecção de bordas (Canny).
        intersection_radius (int): Raio para agrupar interseções próximas.

    Returns:
        dict: Resultados da análise, incluindo número de fraturas e tipos de nós.
        ndarray: Imagem processada com fraturas desenhadas.
    """
    # Carregar a imagem original
    original_image = cv2.imread(image_path)
    
    # Converter para escala de cinza
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Suavizar ruído
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Detectar texto e números (opcional: usando morfologia ou OCR)
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morphed = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    # Criar uma máscara para ignorar regiões com texto
    mask = cv2.bitwise_not(morphed)  # Inverter a máscara para filtrar texto
    filtered_image = cv2.bitwise_and(blurred, blurred, mask=mask)

    # Detectar bordas usando Canny na imagem filtrada
    lower_threshold = sensitivity
    upper_threshold = sensitivity * 3
    edges = cv2.Canny(filtered_image, lower_threshold, upper_threshold)

    # Detectar linhas usando a Transformada de Hough
    min_line_length = 30  # Ignorar linhas muito curtas
    max_line_gap = 15     # Conectar segmentos próximos
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=min_line_length, maxLineGap=max_line_gap)

    # Criar uma cópia da imagem original para desenhar as fraturas detectadas
    processed_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)  # Converter de volta para RGB para desenhar
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(processed_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Linhas desenhadas em verde

    # Detectar interseções e classificar os nós
    intersections = find_intersections(lines) if lines is not None else []
    node_counts = analyze_intersections(intersections, intersection_radius)

    # Retornar resultados e imagem processada
    return {"fraturas": len(lines) if lines is not None else 0, **node_counts}, processed_image

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