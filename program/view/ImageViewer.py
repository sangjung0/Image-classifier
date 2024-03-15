from PyQt5.QtGui import QResizeEvent, QBrush, QShowEvent
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt
import time

from view.Base import Base

class ImageViewer(Base):
    def __init__(self, uiPath:str, **kwargs) -> None:
        super().__init__(uiPath, **kwargs)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(Qt.black))

        self.graphicsView.setScene(self.scene)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__width = 0
        self.__height = 0

        self.__init()
        self.__setEvent()

    def __init(self):
        self.fileNameLabel.setText("name")
        self.filePathLabel.setText("path")
        self.gpsLabel.setText("gps")
        self.datetimeLabel.setText("datetime")

    def __setEvent(self):
        self.nextButton.clicked.connect(self._setImage)
        self.prevButton.clicked.connect(self._setImage)
        self.openFolderButton.clicked.connect(self._setImage)

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.__onResize()
        return super().showEvent(a0)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.__onResize()
        return super().resizeEvent(a0)
    
    def __onResize(self):
        self.__width = self.graphicsView.width()
        self.__height = self.graphicsView.height()
        self.scene.setSceneRect(0,0,self.__width, self.__height)
        self._setImage()

    def _setImage(self):
        if not self.allImgPath:
            return
        while True:
            image = self.imageBuffer.getImage(self.allImgPath[self._index])
            if image:

                width = self.__width
                height = self.__height

                pixmapSize = image.pixmap.size()
                scale = min(width / pixmapSize.width(), height / pixmapSize.height())
                if scale < 1:
                    scaledPixmap = image.pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                else:
                    scaledPixmap = image.pixmap
                
                # 조정된 이미지를 scene에 중앙 정렬로 추가합니다.
                self.scene.clear()
                item = self.scene.addPixmap(scaledPixmap)
                item.setPos((width - scaledPixmap.width()) / 2, (height - scaledPixmap.height()) / 2)
                self.update()

                self._setFileName(image.path.name)
                self._setFilePath(image.path)
                self._setDatetime(image.datetime)
                self._setGps(image.gps)

                break
            time.sleep(0.1)