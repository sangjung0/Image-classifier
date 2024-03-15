from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QPushButton, QLabel, QVBoxLayout, QScrollArea, QWidget
from threading import Thread
from datetime import datetime

from util.util import Loger

from view.ImageBuffer import ImageBuffer

class Base(QMainWindow):
    def __init__(self, uiPath:str, **_) -> None:
        super().__init__()
        uic.loadUi(uiPath, self)

        self.graphicsView:QGraphicsView
        self.nextButton:QPushButton
        self.prevButton:QPushButton
        self.openFolderButton:QPushButton
        self.countLabel:QLabel
        self.pathLabel:QLabel
        self.datetimeLabel:QLabel
        self.fileNameLabel:QLabel
        self.filePathLabel:QLabel
        self.gpsLabel:QLabel
        self.rightCenter:QVBoxLayout
        self.addButton:QPushButton
        self.scrollArea:QScrollArea
        self.scrollAreaWidgetContents:QWidget

        self.fileNameLabel.setWordWrap(True)
        self.filePathLabel.setWordWrap(True)
        self.datetimeLabel.setWordWrap(True)
        self.gpsLabel.setWordWrap(True)

        self.loger = Loger("gui", True)

        self.path:Path = None
        self.allImgPath:list[Path] = None
        self._totalFiles:int = 0
        self._index:int = -1
        self.imageBuffer:ImageBuffer = ImageBuffer()
        self.imageBufferTh:Thread = None

        
    def _setCountLabel(self, value:int):
        self.countLabel.setText(f"({value:>5}:{self._totalFiles:<5})")

    def _setFileName(self, value:str):
        self.fileNameLabel.setText(f"name: {value if value else ''}")

    def _setFilePath(self, value:Path):
        self.filePathLabel.setText(f"path: {str(value) if value else ''}")

    def _setDatetime(self, value:datetime):
        self.datetimeLabel.setText(f"date: {value.strftime('%Y-%m-%d %H-%M-%S') if value else ''}")

    def _setGps(self, value):
        self.gpsLabel.setText(f"gps: {value if value else ''}")