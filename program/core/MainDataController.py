import pathlib
from threading import Lock


from program.core.Storage import Storage
from program.core.AutoSave import AutoSave
from program.core.DataController import DataController
from program.core.scheduler import Scheduler

class MainDataController(DataController):
    def __init__(self, path: pathlib.Path):
        self.__storage:Storage
        self.__auto_save:AutoSave
        self.__scheduler:Scheduler
        self.__lock:Lock

        super().__init__()

    def organization(self) : pass

    def add_path(self, add_path:pathlib.Path): pass