from PyQt5.QtWidgets import  QWidget, QMessageBox
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import QThread, pyqtSignal
import pathlib

from gui import ImagePanel
from gui.imageLayer.interactiveObject import *
from gui.pathModal import AddPath
from gui.imageLayer.ImageLayer import ImageLayer

from core import MainDataController

from gui.Utils import message_box

class MainImageLayer(ImageLayer):
    """메인 레이어 만드는 클래스 오직 한개만 생성 되야 함"""
    def __init__(self, base:QWidget, image_panel: ImagePanel, data_controller:MainDataController) -> None:
        super().__init__(base, image_panel, data_controller)
        self.__data_controller:MainDataController = data_controller
        self.__new_folder: NewFolder = NewFolder(self, self.__new_folder_event)
        self.__auto_save: AutoSave = AutoSave(self, self.__auto_organization)
        self.__add_path: AddPath = AddPath(self, self.__add_folder_event)
        
        self.th = None
        
    def resizeEvent(self, event:QResizeEvent) -> None:
        size = event.size()
        self.__new_folder.resize_event(size)
        self.__auto_save.resize_event(size)
        super().resizeEvent(event)
        
    def hide_event(self)->None:
        self.__new_folder.hide()
        self.__auto_save.hide()
        super().hide_event()
    
    def show_event(self) ->None:
        self.__new_folder.show()
        self.__auto_save.show()
        super().show_event()

    def __new_folder_event(self) -> None:
        self.__add_path.show(self.mapToGlobal(self.geometry().center()))
        
    def __add_folder_event(self, path:pathlib.Path) -> None:
        if self.__data_controller.sub_path_is_full():
            message_box(self, "add path error", "sub path is full")
        else: self.__data_controller.add_path(path)
        
    def __auto_organization(self) -> None:
        if self.th is not None:
            message_box(self, "organization error", "Auto-saving is currently in progress")
            return
        self.th = Worker(self.__data_controller.organization)
        self.th.finished.connect(self.__th_clear)
        self.th.start()
        
    def __th_clear(self) -> None:
        message_box(self, "organization Done", "Auto-saving is Done", b_type=QMessageBox.Information)
        self.th = None
        
class Worker(QThread):
    finished = pyqtSignal()
    def __init__(self, work):
        super().__init__()
        self.work = work

    def run(self):
        self.work()
        self.finished.emit()