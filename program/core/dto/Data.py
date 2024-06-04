import pathlib
import threading

from core.dto.Face import Face
from core.dto.Image import Image

class Data:
    
    __MAX_FACE:int = 10
    
    def __init__(self):
        self.__image: dict[pathlib.Path: Image] = dict()
        self.__name: dict[int: str] = dict()
        self.__faces: dict[int: list[Face]] = dict()
        self.__lock:threading.Lock = threading.Lock()

    def saerch(self, paths:list[pathlib.Path]):
        thread = threading.Thread(target=self, args=(paths,))
        thread.start()

    def __call__(self, paths:list[pathlib.Path]):
        for path in paths:
            if not path in self.__image:
                with self.__lock:
                    self.__image[path] = Image(path)                

    def get_image(self, path: pathlib.Path) -> Image:
        return self.__image[path]

    def get_name(self, name: int) -> str:
        return self.__name[name]

    def get_face(self, n: int) -> list[Face]:
        return self.__faces[n]

    def set_face(self, n: int, face: Face) -> None:
        self.__faces[n].append(face)
        if(len(self.__faces[n]) > Data.__MAX_FACE):
            self.__faces[n].pop(0)

    def set_images(self, images: list[Image]) -> None:
        for image in images:
            self.__image[image.get_path()] = image
