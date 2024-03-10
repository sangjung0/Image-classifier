from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem
from pathlib import Path

from view.ImageButton import ImageButton

class Folder(QVBoxLayout):
    def __init__(self, path:Path, files:list[Path], callback:callable):
        super().__init__()
        self.path:path = path
        self.__name:str = path.name
        self.__number:int = len(files)
        self.__isOpen:bool = False
        self.files:list[ImageButton] = [ImageButton(f,callback) for f in files]
        self.callback = callback

        self.folderNameLabel = QLabel()
        self.pathLabel = QLabel()
        self.countLabel = QLabel()
        self.fileSpace = QSpacerItem(20,0)
        self.fileLayout = QHBoxLayout()
        self.fileList = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.labelLayout = QVBoxLayout()
        self.openButton = QPushButton()
        self.addButton = QPushButton("add")

        self.folderNameLabel.setWordWrap(True)
        self.pathLabel.setWordWrap(True)
        self.countLabel.setWordWrap(True)
        self.addButton.setStyleSheet("QPushButton { padding: 1px; margin: 1px;}")

        for f in self.files:
            self.fileList.addWidget(f)

        self.labelLayout.addWidget(self.folderNameLabel)
        self.labelLayout.addWidget(self.pathLabel)
        self.labelLayout.addWidget(self.countLabel)
        self.buttonLayout.addLayout(self.labelLayout,8)
        self.buttonLayout.addWidget(self.addButton,2)
        self.addLayout(self.buttonLayout)
        self.fileLayout.addItem(self.fileSpace)
        self.fileLayout.addLayout(self.fileList)
        self.addLayout(self.fileLayout)
        self.addWidget(self.openButton)

        self.folderNameLabel.setText(str(self.__name))
        self.pathLabel.setText(str(path))
        self.setCount(self.__number)
        
        self.openButton.clicked.connect(self.__close)
        self.__close()

    def __open(self):
        for f in self.files:
            f.show()
        self.openButton.setText("close")
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.__close)

    def __close(self):
        for f in self.files:
            f.hide()
        self.openButton.setText("open")
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.__open)

    def append(self, path:Path):
        if not path in self.files:
            self.files.append(ImageButton(path, self.callback))
            self.__number += 1

    def pop(self, path:Path):
        if path in self.files:
            self.files = filter(lambda x: x.path == path, self.files)
            self.__number -= 1

    def setCount(self, value:int):
        self.countLabel.setText(f"number: {value}")

    