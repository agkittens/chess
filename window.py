import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout


class Popup(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Popup Window')

        layout = QVBoxLayout()
        self.setLayout(layout)

    # def update_queue(self, list):
