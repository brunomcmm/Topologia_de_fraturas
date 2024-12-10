"""
main.py

Módulo principal para inicializar o Analisador de Fraturas. 
Este arquivo é responsável por carregar e exibir a interface gráfica da aplicação.
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui import FractureAnalyzerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FractureAnalyzerApp()
    window.show()
    sys.exit(app.exec_())