from pathlib import Path
from PyQt5.QtWidgets import QFileDialog

from image_data import PathData

from view.Base import Base

class PathController(Base):
    def __init__(self, uiPath:str, **kwargs) -> None:
        super().__init__(uiPath, **kwargs)

        self.__init()
        self.__setButton()

    def __setButton(self):
        self.openFolderButton.clicked.connect(self.__openFile)

    def __init(self) -> None:
        self.pathLabel.setText("")

    def __openFile(self) -> None:
        fname = QFileDialog.getExistingDirectory(self, 'Open folder', './')
        fname = Path(fname)
        if fname.exists() and fname.is_dir():
            self.path = fname
            self.pathLabel.setText(str(fname))
            self.allImgPath = [i for i in PathData(fname)]
            self._totalFiles = len(self.allImgPath)
            self._index = -1
            if not self._totalFiles:
                return #역시나 에러처리 해야 됨
            self.loger(f"파일 경로 설정 됨: {self.path}")
        else:
            self.loger(f"파일 경로 설정 실패: {fname}") 
            #에러처리 해야 함

