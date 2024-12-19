# Topologia de Fraturas

Este programa identifica fraturas em imagens utilizando técnicas de processamento digital e análise de interseções. É uma ferramenta robusta que permite classificar e analisar padrões topológicos de fraturas em imagens, fornecendo insights detalhados sobre suas características.

## Funcionalidades
- Conversão de imagens: Transforma as imagens para escala de cinza, otimizando a detecção de fraturas.
- Detecção de fraturas: Utiliza a Transformada de Hough para identificar linhas representando fraturas na imagem.
- Classificação de nós: Identifica e classifica interseções de fraturas como tipos X, Y ou I.
- Exportação de resultados: Salva as análises em arquivos .txt para consultas posteriores.
- Visualização interativa: Gera uma pré-visualização da imagem processada com as fraturas identificadas.

## Módulos
1. **`main.py`**:
- Gerencia a execução principal do programa.
- Coordena a análise e visualização das imagens processadas.
2. **`gui.py`**:
- Implementa a interface gráfica para facilitar a interação com o programa.
3. **`image_processing.py`**:
- Realiza o processamento básico das imagens, incluindo a conversão para escala de cinza e aplicação de filtros.
4. **`intersection_utils.py`**:
- Contém funções para identificar e classificar os tipos de interseções entre as fraturas.
5. **`analysis.py`**:
- Responsável pela análise dos dados processados, incluindo cálculos e classificações.

## Como Usar

1. Clone o repositório:
```bash 
git clone https://github.com/brunomcmm/Topologia_de_fraturas.git
```

