import pathlib
import threading

from core.dto.Face import Face
from core.dto.Image import Image

class Data:
    """
    DataController의 데이터를 관리함
    이미지, 이름, 얼굴 데이터를 가지고 있음.
    """
    
    __MAX_FACE:int = 3
    
    def __init__(self) -> None:
        self.__image: dict[pathlib.Path, Image] = dict()
        self.__name: dict[int, str] = dict()
        self.__faces: dict[int, list[Face]] = dict()
        self.__lock:threading.Lock = threading.Lock()
        
        self.__flag:bool = False
        self.__thread:threading.Thread = None
        
    @property
    def faces(self) -> dict[int, list[Face]]:
        return self.__faces
    
    @property
    def name(self) -> dict[int, str]:
        return self.__name
    
    def init(self)->None:
        for image in self.__image.values():
            if not image.is_detected:
                image.is_scheduled = False

    def search(self, paths:list[pathlib.Path]) -> None:
        """
        Thread를 통하여 이미지 데이터를 가져옴
        """
        self.__thread = threading.Thread(target=self, args=(paths,))
        self.__thread.start()

    def __call__(self, paths:list[pathlib.Path]) -> None:
        for path in paths:
            if self.__flag: break
            if not path in self.__image and path.exists():
                image = Image(path)
                with self.__lock:
                    self.__image[path] = image
                
    def close(self) -> None:
        self.__flag = True
        if self.__thread != None:
            self.__thread.join()

    def get_image(self, path: pathlib.Path) -> Image:
        if path in self.__image:
            return self.__image[path]
        image = Image(path)
        with self.__lock:
            self.__image[path] = image
        return image

    def add_images(self, images: list[Image]) -> None:
        for image in images: 
            self.__image[image.get_path()] = image
        
    def set_face(self, n: int, face: Face) -> None:
        if n in self.__faces: self.__faces[n].append(face)
        else: self.__faces[n] = [face]
        if(len(self.__faces[n]) > Data.__MAX_FACE):
            self.__faces[n].pop(0)
            
    def delete(self, src:pathlib.Path) -> None:
        with self.__lock:
            del self.__image[src]
        
    def __getstate__(self):
        state = self.__dict__.copy()
        
        del state['_Data__lock']
        del state['_Data__thread']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        
        self.__lock:threading.Lock = threading.Lock()
        self.__thread:threading.Thread = None