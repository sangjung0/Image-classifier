import pathlib
from threading import Lock


from core.Storage import Storage
from core.AutoSave import AutoSave
from core.DataController import DataController
from core.scheduler import Scheduler
from core.dto import Data

from utils import PathData

class MainDataController(DataController):
    
    __MAX_PATH_COUNT:int = 4
    
    def __init__(self, path: pathlib.Path, sub_path:list[pathlib.Path] = []):
        paths = list(PathData(path))
        data = Data()
        data.search(paths)
        super().__init__(paths, sub_path, data)
        self.__sub_path:list[pathlib.Path] = sub_path
        
        self.__storage:Storage
        self.__auto_save:AutoSave
        self.__scheduler:Scheduler
        self.__lock:Lock

    def organization(self) : pass

    def add_path(self, add_path:pathlib.Path) -> None:
        if len(self.__sub_path) >= MainDataController.__MAX_PATH_COUNT: raise Exception()
        self.__sub_path.append(add_path)
        
    def sub_path_is_full(self) -> bool:
        if len(self.__sub_path) >= MainDataController.__MAX_PATH_COUNT: return True
        return False 