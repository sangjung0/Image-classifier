from PyQt5.QtWidgets import  QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QResizeEvent, QWheelEvent, QCloseEvent

from gui.imageLayer.interactiveObject import *
from gui import ImagePanel

from core import DataController


class ImageLayer(QWidget):
    def __init__(self, base:QWidget, image_panel: ImagePanel, data_controller:DataController) -> None:
        super().__init__(base)
        self.__image_panel: ImagePanel = image_panel
        self.__image_data_viewer: ImageDataViewer = ImageDataViewer(self, lambda : 0, 0.01, 0.99, 300,100, (0, -100))
        self.__prev:Prev = Prev(self, self.__prev_event, 0, 0.5, 100, 50, (40, -25))
        self.__next:Next = Next(self, self.__next_event, 1, 0.5, 100, 50, (-140, -25))
        self.__data_controller:DataController = data_controller# 종속성 추가
        
        # 이벤트 관련 변수
        self.__ctrl_pressed:bool = False
        self.__prev_pos:QPoint = None
        self.__wheel_pressed:bool = False
        self.__move_event:QPoint = None
        self.__modal_is_exist:bool = False
        self.__modal:QWidget = None
        
        self.setFocus()
        self.__next_event()
        

    def __next_event(self) -> None:
        image, ary = self.__data_controller.get_next_image()
        self.__image_panel.set_image(image.characters, ary)
        self.__image_data_viewer.set_data(image.name, image.date, image.path)
        
    def __prev_event(self) -> None:
        image, ary = self.__data_controller.get_prev_image()
        self.__image_panel.set_image(image.characters, ary)
        self.__image_data_viewer.set_data(image.name, image.date, image.path)

    def __file_move_event(self, pos:QPoint) -> None:
        dx = pos.x()
        dy = pos.y()
        if abs(dx) > abs(dy):
            if dx > 100:
                self.__data_controller.move(0)
            elif dx < -100:
                self.__data_controller.move(1)
        else:
            if dy > 100:
                self.__data_controller.move(2)
            elif dy < -100:
                self.__data_controller.move(3)
                        
    def __search_modal(self, controller:DataController) -> None:
        if controller is None:
            print("검색 된 거 없음")
            return
        pos = self.pos()
        size = self.size()
        try:
            from gui import Frame
            self.__modal = Frame(pos.x(), pos.y(), size.width(), size.height(), data_controller=controller)
            self.__modal.show()
        except Exception as e:
            print(e)
        print("이미지 검색")
                
    def __button_rander(self, b:bool) -> None: pass
    
    # -- 이벤트 함수 -- #
    
    def closeEvent(self, event:QCloseEvent) -> None:
        self.__data_controller.close()
        super().closeEvent(event)    
    
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

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            num = self.__image_panel.click_event(a0.pos())
            if num == None:self.__search_modal(self.__data_controller.search_image())
            else: self.__search_modal(self.__data_controller.search_face(num))
        super().mouseDoubleClickEvent(a0)
        
    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.MiddleButton:
            self.__prev_pos = a0.pos()
            self.__wheel_pressed = True
        elif a0.button() == Qt.MouseButton.LeftButton:
            self.__move_event = a0.pos()
        super().mousePressEvent(a0)
        
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.MiddleButton:
            self.__wheel_pressed = False
        elif a0.button() == Qt.MouseButton.LeftButton:
            self.__file_move_event(a0.pos() - self.__move_event)
        super().mouseReleaseEvent(a0)
        
    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.__wheel_pressed:
            pos = a0.pos()
            self.__image_panel.image_move(pos - self.__prev_pos)
            self.__prev_pos = pos
        super().mouseMoveEvent(a0)


