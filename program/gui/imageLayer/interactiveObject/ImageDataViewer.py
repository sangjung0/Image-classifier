import datetime
import pathlib
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QSize

from Constant import IMAGE_DATA_VIEWER_HEIGHT, IMAGE_DATA_VIEWER_WIDTH, IMAGE_DATA_VIEWER_X_RATIO, IMAGE_DATA_VIEWER_Y_RATIO

class ImageDataViewer(QWidget):
    """QWidget을 상속받는 이미지 데이터를 표시하는 클래스"""

    def __init__(self, 
                 base:QWidget, 
                 x_ratio: float = IMAGE_DATA_VIEWER_X_RATIO, 
                 y_ratio: float = IMAGE_DATA_VIEWER_Y_RATIO, 
                 width: int = IMAGE_DATA_VIEWER_WIDTH,
                 height: int = IMAGE_DATA_VIEWER_HEIGHT, 
                 axes:tuple[int] = (0, 0)) -> None:
        super().__init__(base)
        
        self.__x_ratio: float = x_ratio
        self.__y_ratio: float = y_ratio
        self.__axes: tuple[int] = axes
        self.__width: int = width
        self.__height: int = height
        
        self.__name:QLabel = QLabel(self)
        self.__date:QLabel = QLabel(self)
        self.__path:QLabel = QLabel(self)
        
        self.__name.setMargin(2)
        self.__date.setMargin(2)
        self.__path.setMargin(2)
        self.__path.setWordWrap(True)
        self.setStyleSheet("background-color: rgba(0,0,0,100); color: white;")
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.__name, 1)
        layout.addWidget(self.__date, 1)
        layout.addWidget(self.__path, 2)
        
        self.setLayout(layout)
        
        self.setGeometry(0, 0, self.__width, self.__height)
        self.set_data("None", datetime.datetime.now(), pathlib.Path("/image/"))

    def resize_event(self, size:QSize) -> None:
        """
        크기에 따라 x, y 값 비율로 위치 조정
        
        size: QSize
        """

        self.move(int(size.width() * self.__x_ratio) + self.__axes[0], int(size.height() * self.__y_ratio + self.__axes[1]))

    def set_data(self, name: str, dt: datetime.datetime, path: pathlib.Path) -> None:
        self.__name.setText(name)
        self.__date.setText(str(dt))
        self.__path.setText(str(path))
    
    