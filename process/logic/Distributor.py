from PIL import Image as Img
from PIL.ExifTags import GPSTAGS
from pathlib import Path
from typing import Iterable
import numpy as np
import cv2
from datetime import datetime as dt

from process.logic.StartPointInterface import StartPointInterface

from process.model import Image, Section

GPS = 34856
DATETIME = 306

class Distributor(StartPointInterface):
    def __init__(self, pathData:Iterable[Path], cfl:int):
        self.__pathData = pathData
        self.__cfl = cfl
        self.__iter = None
        self.__setIsFinish = None

    def prepare(self, setIsFinish:callable) -> None:
        self.__iter = iter(self.__pathData)
        self.__setIsFinish = setIsFinish

    def processing(self, section:Section) -> Section:
        it = self.__iter
        cfl = self.__cfl

        try:
            while True:
                path = next(it)
                img, gps, datetime = self.getInfo(path)
                print(gps, datetime)
                section.append(Image(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), path))
                if len(section) >= cfl:
                    break
        except StopIteration:
            self.__setIsFinish(True)
        except Exception as e:
            raise e
        return section
    
    def getInfo(self, path:Path):
        img = Img.open(str(path))
        exif = img.getexif()
        if not exif:
            return np.array(img), None, None
        
        gps = None
        if GPS in exif:
            gps = {}
            for t, value in GPSTAGS.items():
                if t in exif[GPS]:
                    gps[value] = exif[GPS][t]
        
        datetime = None
        if DATETIME in exif:
            datetime = dt.strptime(exif[DATETIME],"%Y:%m:%d %H:%M:%S")

        return np.array(img), gps, datetime
    
        
