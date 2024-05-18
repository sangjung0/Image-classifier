from datetime import datetime as dt
from pathlib import Path

from image_data.model.Face import Face


class MetaData:
    def __init__(self, index:int, path:Path, face:list[Face], datetime:dt=None, gps=None) -> None:
        self.__index = index
        self.__path = path
        self.__face = face
        self.__datetime = datetime
        self.__gps = gps

    @property
    def index(self)->int:
        return self.__index
    @index.setter
    def index(self, value:int)->None:
        self.__index = value
    @property
    def path(self)->Path:
        return self.__path
    @path.setter
    def path(self, value:Path)->None:
        self.__path = value
    @property
    def face(self)->Path:
        return self.__face
    @face.setter
    def face(self, value:Path)->None:
        self.__face = value
    @property
    def datetime(self)->dt:
        return self.__datetime
    @datetime.setter
    def datetime(self, value:dt)->None:
        self.__datetime = value
    @property
    def gps(self):
        return self.__gps
    @gps.setter
    def gps(self, value)->None:
        self.__gps = value