from program.gui import ImagePanel
from program.gui.imageLayer.interactiveObject import *
from program.gui.pathModal import AddPath


class ImageLayer:
    def __init__(self, image_panel: ImagePanel):
        self.__image_panel: ImagePanel
        self.__image_data_viewer: ImageDataViewer
        self.__boundary_boxs: list[BoundaryBox]
        self.__prev:Prev
        self.__next:Next
        self.__path_modal:AddPath
        self._data_controller # 종속성 추가

    def __next_event(self): pass
    def __prev_event(self): pass
    def __set_boundary_box(self): pass
    def __set_image_data(self): pass
    def __set_mouse_event(self): pass
    def __resize_event(self): pass
    def __file_move_event(self): pass
    def __get_data_thread(self): pass
    def _set_button_event(self): pass
    def _button_rander(self, b:bool): pass



