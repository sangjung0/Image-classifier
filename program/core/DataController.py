import pathlib
import numpy as np
import time
import threading
import gc

from core.Searcher import Searcher
from core.dto import Data, Image
from core.Constant import CACHE_SIZE


class DataController:
    """Data를 컨트롤하는 클래스 이미지 검색, 이미지 탐색, 이미지 이동 등을 지원"""
    
    def __init__(self, image_path: list[pathlib.Path], sub_path: dict[int, pathlib.Path], data:Data = None) -> None:
        self.__image_path: list[pathlib.Path] = image_path
        self.__sub_path: dict[int:pathlib.Path] = sub_path
        self.__images: Data = Data() if data is None else data 
        
        self.__searcher: Searcher = Searcher(self.__images, self.__image_path)
        
        self.__cache: dict[pathlib.Path, np.ndarray] = dict()
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
            ary = image.image
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

    def search_image(self) -> 'DataController':
        cnt = self.get_cnt_image()[0]
        if cnt.histogram is None: return None
        paths = self.__searcher.search_image(self.get_cnt_image()[0])
        if len(paths) <= 1: return None
        return DataController(paths, self.__sub_path, self.__images)

    def search_face(self, i:int) -> 'DataController':
        paths = self.__searcher.search_face(self.get_cnt_image()[0].characters[i].name)
        if len(paths) <= 1: return None
        return DataController(paths, self.__sub_path, self.__images)

    def move(self, n: int) -> bool: 
        if n >= len(self.__sub_path): return False
        src = self.__image_path[self._cnt_image_index]
        dest:pathlib.Path = self.__sub_path[n] / src.name
        src.rename(dest)
        self.__images.delete(src)
        self.__image_path[self.__image_path.index(src)] = dest   
        return True
    
    def __image_index(self, value:int) -> None:
        return (self._cnt_image_index + value) % len(self.__image_path)
        
    def __cache_manager(self) -> None:
        """현재 사용자가 보고있는 이미지를 기준으로 미리 이미지 로드"""
        start = CACHE_SIZE//2
        while True:
            time.sleep(0.1)
            if self.__flag: break
            cnt = self._cnt_image_index
            length = len(self.__image_path)
            if length == 0: continue
            a = set(self.__image_path[(cnt+i)%length] for i in range(-start, start, 1))
            b = set(self.__cache.keys())
            a, b = list(b-a), list(a-b)
            i = 0
            while i < len(a) or i < len(b):
                if cnt != self._cnt_image_index:
                    break
                if i < len(a):
                    with self.__lock:
                        del self.__cache[a[i]]
                if i < len (b):
                    image = self.__images.get_image(b[i]).image
                    with self.__lock:
                        self.__cache[b[i]] = image
                i += 1
            gc.collect()
            
    def close(self) -> None:
        self.__flag = True
        if self.__thread != None:
            self.__thread.join()
        self.__images.close() 
            
