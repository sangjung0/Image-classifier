import sys
import pathlib
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from util.util import Loger
from process import Controller, PathData

from view.PathController import PathController
from view.ImageController import ImageController
from view.ImageViewer import ImageViewer
from view.Base import Base

class Main(ImageViewer, ImageController, PathController):
    def __init__(self, uiPath:str, bufSize:int = 20) -> None:
        super().__init__(uiPath = uiPath, bufSize = bufSize)

        self.__init()
        self.__setButton()

    def __init(self) -> None: pass

    def __setButton(self) -> None: pass

    @staticmethod
    def start(fileName:str) -> tuple[QApplication, QMainWindow]:
        app = QApplication([])

        window = Main(fileName)
        window.show()

        return app, window