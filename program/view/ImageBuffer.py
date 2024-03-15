from threading import Lock
from PIL import Image as Img
from PIL.ExifTags import GPSTAGS
from pathlib import Path
import numpy as np
import time
from datetime import datetime as dt

from util.util import Loger
from view.model import Image

GPS = 34856
DATETIME = 306

class ImageBuffer:
    def __init__(self):
        self.__isFinish = False
        self.__lock = Lock()
        self.__path:list[Path] = []
        self.__buf:dict[Path,Image] = {}

    def setIsFinish(self, value:bool):
        with self.__lock:
            if isinstance(value, bool): self.__isFinish = value
            else: raise ValueError("isFinish is must dbe bool")

    def setPath(self, value:list[Path]):
        with self.__lock:
            if isinstance(value, list):
                self.__path = []
                for p in set(value) - set(self.__buf.keys()):
                    self.__path.append(p)
                for p in set(self.__buf.keys()) - set(value):
                    del self.__buf[p]
            else: raise ValueError("path is must be list")

    def getImage(self, path:Path):
        with self.__lock:
            return self.__buf.get(path, None)
        
    def setImage(self, path:Path, image:Image):
        with self.__lock:
            self.__buf[path] = image

    def __call__(self):
        loger = Loger("imageBuffer")
        loger("start",option="start")
        while True:
            if not self.__isFinish:
                if self.__path:
                    path = self.__path.pop()
                    self.setImage(path, Image(path, *self.__getInfo(path)))
                else:
                    time.sleep(0.1)
            else:
                break

    def __getInfo(self, path:Path):
        img = Img.open(str(path))
        exif = img.getexif()
        if not exif:
            return img, None, None
        
        gps = None
        if GPS in exif:
            gps = {}
            for t, value in GPSTAGS.items():
                if t in exif[GPS]:
                    gps[value] = exif[GPS][t]
        
        datetime = None
        if DATETIME in exif:
            datetime = dt.strptime(exif[DATETIME],"%Y:%m:%d %H:%M:%S")

        return img, datetime, gps
    