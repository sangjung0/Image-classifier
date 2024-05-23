import pathlib
import numpy as np

from program.core.dto import Face, Character


class PacketData:
    def __init__(self, path: pathlib.Path):
        self.__path: pathlib.Path
        self.__image: np.ndarray
        self.__hash: bin
        self.__faces: list[Face]
        self.__chracters: list[Character]

    def get_image(self) -> np.ndarray:
        pass

    def get_path(self) -> pathlib.Path: pass

    def get_hash(self) -> bin: pass

    def get_faces(self) -> list[Face]: pass

    def get_chracters(self) -> list[Character]: pass

    def set_face(self, face: Face): pass

    def set_character(self, character: Character): pass

    def set_image(self, image: np.ndarray): pass

    def set_hash(self, hash_: bin): pass
