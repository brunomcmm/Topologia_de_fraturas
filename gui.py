"""
gui.py

Módulo responsável pela interface gráfica do Analisador de Fraturas.
Inclui funcionalidades para selecionar imagens, exibir o preview, ajustar parâmetros,
e exibir os resultados da análise.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QSpinBox, QGroupBox, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from image_processing import process_image  # Importaremos mais tarde

class FractureAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analisador de Fraturas")
        self.setGeometry(100, 100, 1200, 550)  # Janela maior para acomodar os ajustes

        # Configurar a interface principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Criar o painel esquerdo (seleção, status, botões)
        self.left_panel = QVBoxLayout()

        # Caixa de texto para exibir o caminho da imagem selecionada
        self.image_path_box = QLineEdit()
        self.image_path_box.setPlaceholderText("Nenhuma imagem selecionada")
        self.image_path_box.setReadOnly(True)  # Apenas para exibição
        self.left_panel.addWidget(self.image_path_box)

        # Botão para selecionar imagem
        self.select_image_button = QPushButton("Selecionar Imagem")
        self.select_image_button.clicked.connect(self.load_image)
        self.left_panel.addWidget(self.select_image_button)

        # Botão para iniciar a análise
        self.analyze_button = QPushButton("Analisar")
        self.analyze_button.setEnabled(False)  # Inicialmente desativado
        self.analyze_button.clicked.connect(self.analyze_image)
        self.left_panel.addWidget(self.analyze_button)

        # Caixa de texto para status (altura ajustada)
        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)
        self.status_box.setFixedSize(450, 300)  # Largura e altura ajustadas para maior equilíbrio
        self.left_panel.addWidget(self.status_box)

        # Controles para ajustar parâmetros
        self.controls_group = QGroupBox("Parâmetros")
        self.controls_layout = QVBoxLayout()

        self.sensitivity_label = QLabel("Sensibilidade:")
        self.controls_layout.addWidget(self.sensitivity_label)
        self.sensitivity_spinbox = QSpinBox()
        self.sensitivity_spinbox.setRange(1, 100)
        self.sensitivity_spinbox.setValue(100)
        self.controls_layout.addWidget(self.sensitivity_spinbox)

        self.radius_label = QLabel("Raio para interseções:")
        self.controls_layout.addWidget(self.radius_label)
        self.radius_spinbox = QSpinBox()
        self.radius_spinbox.setRange(1, 50)
        self.radius_spinbox.setValue(10)
        self.controls_layout.addWidget(self.radius_spinbox)

        self.controls_group.setLayout(self.controls_layout)
        self.left_panel.addWidget(self.controls_group)

        # Botão para sair
        self.exit_button = QPushButton("Sair")
        self.exit_button.clicked.connect(self.close)
        self.left_panel.addWidget(self.exit_button)

        self.layout.addLayout(self.left_panel)

        # Criar o painel direito (preview da imagem ampliado)
        self.right_panel = QVBoxLayout()

        self.image_label = QLabel("Preview da imagem")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(700, 500)  # Espaço para o preview da imagem mantido
        self.right_panel.addWidget(self.image_label)

        # Ajustar as proporções de cada painel
        self.left_panel_widget = QWidget()
        self.left_panel_widget.setLayout(self.left_panel)
        self.right_panel_widget = QWidget()
        self.right_panel_widget.setLayout(self.right_panel)

        self.layout.addWidget(self.left_panel_widget, 3)  # 3 partes para texto e botões
        self.layout.addWidget(self.right_panel_widget, 4)  # 4 partes para imagem

    def log_status(self, message):
        """Adiciona mensagens na caixa de texto de status com uma linha em branco após cada mensagem."""
        self.status_box.append(message)
        self.status_box.append("")  # Adiciona uma linha em branco

    def load_image(self):
        """Carrega a imagem e habilita o botão Analisar."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione uma imagem", "", "Imagens (*.png *.jpg *.bmp)", options=options
        )
        if file_path:
            # Atualiza a caixa de texto com o caminho da imagem selecionada
            self.image_path_box.setText(file_path)
            self.log_status(f"Imagem carregada: {file_path}")

            # Habilitar o botão Analisar
            self.analyze_button.setEnabled(True)

    def analyze_image(self):
        """Inicia a análise da imagem."""
        file_path = self.image_path_box.text()
        if not file_path:
            self.log_status("Nenhuma imagem selecionada para análise.")
            return

        self.log_status("Processando a imagem...")
        results, processed_image = process_image(file_path, self.sensitivity_spinbox.value(), self.radius_spinbox.value())

        # Atualizar o preview com a imagem processada
        height, width, channel = processed_image.shape
        bytes_per_line = channel * width
        q_image = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))

        # Mostrar os resultados
        self.log_status(f"Análise concluída: {results['fraturas']} fraturas, {results['X-nodes']} X-nodes, "
                        f"{results['Y-nodes']} Y-nodes, {results['I-nodes']} I-nodes.")