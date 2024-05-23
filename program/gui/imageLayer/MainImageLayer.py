from program.gui import ImagePanel
from program.gui.imageLayer.interactiveObject import *
from program.gui.imageLayer.ImageLayer import ImageLayer


class MainImageLayer(ImageLayer):
    def __init__(self, image_panel: ImagePanel):
        super().__init__(image_panel)
        self.__new_folder: NewFolder
        self.__auto_save: AutoSave

    def __new_folder_event(self): pass
