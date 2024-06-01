from PyQt5.QtWidgets import  QWidget
from PyQt5.QtGui import QResizeEvent, QCloseEvent
from PyQt5.QtCore import Qt

from gui import ImagePanel
from gui.imageLayer.interactiveObject import *
from gui.pathModal import AddPath
from gui.imageLayer.ImageLayer import ImageLayer

from core import MainDataController

class MainImageLayer(ImageLayer):
    def __init__(self, base:QWidget, image_panel: ImagePanel, data_controller:MainDataController):
        super().__init__(base, image_panel, data_controller)
        self.__parent = base
        self.__new_folder: NewFolder = NewFolder(self, self.__new_folder_event, 0.5, 0.01, 100, 50, (-110, 0))
        self.__auto_save: AutoSave = AutoSave(self, self.__auto_organization, 0.5, 0.01, 100, 50, (10, 0))
        self.__add_path: AddPath = AddPath(self, self.__add_folder_event)
        
    def resizeEvent(self, event:QResizeEvent):
        size = event.size()
        self.__new_folder.resize_event(size)
        self.__auto_save.resize_event(size)
        super().resizeEvent(event)

    def __new_folder_event(self):
        self.__add_path.show(self.mapToGlobal(self.geometry().center()))
        
    def __add_folder_event(self, path): pass
        
    
    def __auto_organization(self): pass