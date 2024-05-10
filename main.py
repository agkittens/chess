import sys

from PyQt5.QtWidgets import QApplication

from window import Window


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

main()
