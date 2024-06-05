import pathlib
import numpy as np

from core.dto import Face, Character


class PacketData:
    def __init__(self, path: pathlib.Path) -> None:
        self.__path: pathlib.Path = path
        self.__image: np.ndarray = None
        self.__hash: bin = None
        self.__faces: list[Face] = []
        self.__chracters: list[Character] = []

    def get_image(self) -> np.ndarray | bytes:
        return self.__image

    def get_path(self) -> pathlib.Path:
        return self.__path

    def get_hash(self) -> bin:
        return self.__hash

    def get_faces(self) -> list[Face]:
        return self.__faces

    def get_chracters(self) -> list[Character]:
        return self.__chracters
    
    def set_path(self, path:pathlib.Path) -> None:
        self.__path = path

    def set_face(self, face: Face) -> None:
        self.__faces.append(face)

    def set_character(self, character: Character) -> None:
        self.__chracters.append(character)

    def set_image(self, image: np.ndarray | bytes) -> None:
        self.__image = image

    def set_hash(self, hash_: bin) -> None:
        self.__hash = hash_
