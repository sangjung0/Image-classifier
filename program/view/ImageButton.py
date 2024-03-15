from PyQt5.QtGui import QPaintEngine, QPaintEvent, QPainter
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QStyle, QStyleOptionButton
from PyQt5.QtCore import Qt
from pathlib import Path

class ImageButton(QPushButton):
    def __init__(self, path:Path, callback:callable):
        super().__init__(path.name)
        self._path:Path = path
        self.clicked.connect(lambda:callback(path))

        self.setStyleSheet("QPushButton { padding: 1px; margin: 0px;}")

