from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import QSize


class InteractiveObject(QPushButton):
    """
    상호작용 오브젝트 QPushButton 상속
    """
    def __init__(self, name:str, base:QWidget, callback: callable, x_ratio: float, y_ratio: float, width: int, height: int, axes: tuple[int] = (0, 0)) -> None:
        """
        base -- QWidget 부모 widget
        callback -- 이벤트 함수
        x -- x value
        y -- y value
        width -- width vlaue
        height -- height value
        axes -- 위치 조정
        """
        super().__init__(name, base)
        self.__x_ratio: float = x_ratio
        self.__y_ratio: float = y_ratio
        self.__axes: tuple[int] = axes
        self.__width: int = width
        self.__height: int = height
        
        self.clicked.connect(callback)
        self.setGeometry(0, 0, self.__width, self.__height)

    def resize_event(self, size:QSize):
        """
        크기에 따라 x, y 값 비율로 위치 조정
        
        size: QSize
        """

        self.move(int(size.width() * self.__x_ratio) + self.__axes[0], int(size.height() * self.__y_ratio + self.__axes[1]))