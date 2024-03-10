from pathlib import Path
from datetime import datetime as dt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image as Img

class Image:
    def __init__(self, path:Path, img:Img, datetime:dt, gps) -> None:
        self.pixmap= QPixmap.fromImage(QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_RGB888))
        self.path = path
        self.datetime = datetime
        self.face = []
        self.gps = gps
        self.__height, self.__width = img.size[0], img.size[1]

    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height