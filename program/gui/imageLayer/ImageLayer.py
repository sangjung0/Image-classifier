from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QResizeEvent, QWheelEvent

from gui import ImagePanel
from gui.imageLayer.interactiveObject import *

from core import DataController


class ImageLayer(QWidget):
    def __init__(self, base:QWidget, image_panel: ImagePanel, data_controller:DataController) -> None:
        super().__init__(base)
        self.__image_panel: ImagePanel = image_panel
        self.__image_data_viewer: ImageDataViewer = ImageDataViewer(self, lambda : 0, 0.01, 0.99, 300,100, (0, -100))
        self.__boundary_boxs: list[BoundaryBox]
        self.__prev:Prev = Prev(self, self.__prev_event, 0, 0.5, 100, 50, (40, -25))
        self.__next:Next = Next(self, self.__next_event, 1, 0.5, 100, 50, (-140, -25))
        self._data_controller:DataController = data_controller# 종속성 추가
        
        self.setFocus()
        
        # 이벤트 관련 변수
        self.__ctrl_pressed:bool = False
        self.__prev_pos:QPoint = None
        self.__wheel_pressed:bool = False
    

    def __next_event(self) -> None:
        # 테스트
        print("next")
        
    def __prev_event(self) -> None:
        # 테스트
        print("prev")
        
    def __set_boundary_box(self) -> None: pass
    def __set_image_data(self) -> None: pass
    def __set_mouse_event(self) -> None: pass
    def __resize_event(self) -> None: pass
    def __file_move_event(self) -> None: pass
    def __get_data_thread(self) -> None: pass
    def _set_button_event(self) -> None: pass
    def _button_rander(self, b:bool) -> None: pass
    
    # -- 이벤트 함수 -- #
    
    def resizeEvent(self, event:QResizeEvent) -> None:
        size = event.size()
        self.__next.resize_event(size)
        self.__prev.resize_event(size)
        self.__image_data_viewer.resize_event(size)
        super().resizeEvent(event)
        
    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if a0.key() == Qt.Key.Key_Control:
            self.__ctrl_pressed = True
        super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent | None) -> None:
        if a0.key() == Qt.Key.Key_Control:
            self.__ctrl_pressed = False
        super().keyReleaseEvent(a0)

    def wheelEvent(self, a0: QWheelEvent | None) -> None:
        if self.__ctrl_pressed:
            self.__image_panel.resize_image(a0.angleDelta().y(), a0.pos())
        super().wheelEvent(a0)
        
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.MiddleButton:
            self.__prev_pos = a0.pos()
            self.__wheel_pressed = True
        super().mousePressEvent(a0)
        
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.MiddleButton:
            self.__wheel_pressed = False
        super().mouseReleaseEvent(a0)
        
    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.__wheel_pressed:
            pos = a0.pos()
            self.__image_panel.image_move(pos - self.__prev_pos)
            self.__prev_pos = pos
        super().mouseMoveEvent(a0)


