import pathlib
import numpy as np


from core.Storage import Storage
from core.AutoSave import AutoSave
from core.DataController import DataController
from core.scheduler import Scheduler
from core.dto import  Image
from core.Constant import SCHEDULER_BUF_SIZE, SCHEDULER_MAX_PATH_COUNT, SCHEDULER_PACKET_SIZE

from utils import PathData

class MainDataController(DataController):
    """데이터 컨트롤러를 상속받는 메인 컨트롤러"""
    
    def __init__(self, path: pathlib.Path, sub_path:dict[int,pathlib.Path] = {}) -> None:
        storage = Storage(path)
        paths = list(PathData(path))
        data = storage.load()
        data.search(paths)
        super().__init__(paths, sub_path, data)
        self.__sub_path:dict[int,pathlib.Path] = sub_path
        
        self.__storage:Storage = storage
        self.__auto_save:AutoSave = AutoSave(path, paths, data)
        self.__scheduler:Scheduler = Scheduler(data, paths)
        
        self.__scheduler.run(SCHEDULER_BUF_SIZE, SCHEDULER_PACKET_SIZE)
        
    def get_cnt_image(self) -> tuple[Image, np.ndarray]:
        image, ary = super().get_cnt_image()
        if not image.is_scheduled:
            self.__scheduler.add(image.path)
        return image, ary

    def organization(self):
        self.__auto_save.organization()

    def add_path(self, add_path:pathlib.Path) -> None:
        if len(self.__sub_path) >= SCHEDULER_MAX_PATH_COUNT: raise Exception()
        self.__sub_path.append(add_path)
        
    def sub_path_is_full(self) -> bool:
        if len(self.__sub_path) >= SCHEDULER_MAX_PATH_COUNT: return True
        return False 
    
    def close(self) -> None:
        self.__scheduler.close()
        self.__storage.save()
        super().close()