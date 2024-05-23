import pathlib
import datetime
import numpy as np

from program.core.dto.Character import Character


class Image:
    def __init__(self, path: pathlib.Path):
        self.__path: pathlib.Path
        self.__name: str
        self.__date: datetime.datetime
        self.__time: datetime.time
        self.__characters: tuple[Character]
        self.__hash: bin
        self.__is_detected: bool

    def get_path(self) -> pathlib.Path:
        pass

    def get_name(self) -> str:
        pass

    def get_data(self) -> datetime.datetime:
        pass

    def get_time(self) -> datetime.time:
        pass

    def get_characters(self) -> tuple[Character]:
        pass

    def get_hash(self) -> bin:
        pass

    def get_image(self) -> np.ndarray:
        pass

    def is_detected(self) -> bool:
        pass

    def set_characters(self, characters: tuple[Character]):
        pass

    def set_is_detected(self, b: bool):
        pass

    def set_hash(self, _hash: bin):
        pass
