import pathlib
import numpy as np
import time
import threading

from core.Searcher import Searcher
from core.dto import Data, Image


class DataController:
    
    __CACHE_SIZE:int = 11
    
    def __init__(self, image_path: list[pathlib.Path], sub_path: dict[int: pathlib.Path], data:Data = Data()):
        self.__image_path: list[pathlib.Path] = image_path
        self.__images: Data = data
        self.__sub_path: dict[int:pathlib.Path] = sub_path
        
        self.__searcher: Searcher
        
        self.__cache: dict[pathlib.Path: np.ndarray] = dict()
        self._cnt_image_index:int = 0
        
        self.__lock:threading.Lock = threading.Lock()
        self.__flag:bool = False
        
        # cache manager
        self.__thread:threading.Thread = threading.Thread(target = self.__cache_manager)
        self.__thread.start()


    def get_cnt_image(self) -> tuple[Image, np.ndarray]:
        if(self._cnt_image_index < 0): return None
        path = self.__image_path[self._cnt_image_index]
        image = self.__images.get_image(path)
        if(path in self.__cache):
            ary = self.__cache[path]
        else:
            ary = image.get_image()
            self.__cache[path] = ary                
        return image, ary

    def get_next_image(self) -> tuple[Image, np.ndarray]:
        if(self._cnt_image_index < 0): return None
        self._cnt_image_index = self.__image_index(1)
        return self.get_cnt_image()

    def get_prev_image(self) -> tuple[Image, np.ndarray]:
        if(self._cnt_image_index < 0): return None
        self._cnt_image_index = self.__image_index(-1)
        return self.get_cnt_image()

    def search_image(self) -> 'DataController': pass

    def search_face(self) -> 'DataController': pass

    def stop_search(self): pass

    def move(self, n: int): 
        src = self.__image_path[self._cnt_image_index]
        dest:pathlib.Path = self.__sub_path[n] / src.name
        src.rename(dest)
        self.__images.delete(src)
        index = self.__image_path.index(src)
        self.__image_path[index] = dest
        
    
    def __image_index(self, value:int) -> None:
        return (self._cnt_image_index + value) % len(self.__image_path)
        
    def __cache_manager(self) -> None:
        start = DataController.__CACHE_SIZE//2
        while True:
            time.sleep(0.1)
            if self.__flag: break
            cnt = self._cnt_image_index
            length = len(self.__image_path)
            a = set(self.__image_path[(cnt+i)%length] for i in range(-start, start, 1))
            b = set(self.__cache.keys())
            a, b = b-a, a-b
            i = 0
            while i < len(a):
                if cnt != self._cnt_image_index:
                    break
                with self.__lock:
                    del self.__cache[b[i]]
                image = self.__images.get_image(a[i])
                with self.__lock:
                    self.__cache[a[i]] = image
                    
    def close(self) -> None:
        self.__flag = True
        if self.__thread != None:
            self.__thread.join()
                
            
