from PyQt5.QtGui import QResizeEvent, QShowEvent
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from pathlib import Path

from view.Folder import Folder
from view.ImageController import ImageController
from view.ImageViewer import ImageViewer

class FolderController(ImageViewer, ImageController):
    def __init__(self, uiPath: str, **kwargs) -> None:
        super().__init__(uiPath, **kwargs)

        self.folders:list[Folder] = []
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.__setButton()

    def __setButton(self):
        self.addButton.clicked.connect(self.__add)
        self.openFolderButton.clicked.connect(lambda : self.add(self.path, self.allImgPath))

    def __add(self):
        path = QFileDialog.getExistingDirectory(self, "폴더 선택")
        path = Path(path)
        if path.exists() and path.is_dir():
            self.add(path)
        else: pass # 에러처리 경고창 같은거 하면 될 듯

    def __setIndex(self, path:Path):
        self._index = self.allImgPath.index(path) - 1
        self._next()
        self._setImage()
    
    def showEvent(self, a0: QShowEvent | None) -> None:
        self.resizeEvent(None)
        return super().showEvent(a0)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.scrollAreaWidgetContents.setMaximumWidth(self.scrollArea.width() - 10)
        return super().resizeEvent(a0)

    def add(self, path:Path, files:list[Path] = []):
        folder = Folder(path, files, self.__setIndex)
        self.folders.append(folder)
        self.rightCenter.insertLayout(0, folder)

    