from threading import Thread

from PyQt5.QtGui import QCloseEvent

from view.Base import Base

class ImageController(Base):
    def __init__(self, uiPath:str, bufSize:int, **kwargs) -> None:
        super().__init__(uiPath, **kwargs)

        self.__bufSize = bufSize
        self.__init()
        self.__setButton()

    def __init(self):
        self._setCountLabel(0)
        self.prevButton.setEnabled(False)
        self.nextButton.setEnabled(False)

    def __setButton(self):
        self.prevButton.clicked.connect(self._prev)
        self.nextButton.clicked.connect(self._next)
        self.openFolderButton.clicked.connect(self.__enableImageChangeButton)

    def __enableImageChangeButton(self):
        if self._totalFiles:
            self._setThread()
            self._next()
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.imageBuffer.setIsFinish(True)
        if self.imageBufferTh: self.imageBufferTh.join()
        return super().closeEvent(a0)

    def _next(self) -> None:
        if self._index + 1 < self._totalFiles: self._index += 1
        else: self._index = 0
        
        if self._index >= 0:
            self._setCountLabel(self._index + 1)
            self._setBuf()

    def _prev(self) -> None:
        if self._index - 1 > 0: self._index -= 1
        else: self._index = self._totalFiles - 1

        if self._index >= 0:
            self._setCountLabel(self._index + 1)
            self._setBuf()

    def _setBuf(self):
        bf = self.__bufSize // 2
        f = (self._index + self._totalFiles - bf) % self._totalFiles
        s = (self._index + bf) % self._totalFiles
        if f < s: self.imageBuffer.setPath(self.allImgPath[f:s])
        else: self.imageBuffer.setPath(self.allImgPath[f:] + self.allImgPath[:s])

    def _setThread(self):
        if not self.imageBufferTh:
            self.imageBufferTh = Thread(target=self.imageBuffer)
            self.imageBufferTh.start()

