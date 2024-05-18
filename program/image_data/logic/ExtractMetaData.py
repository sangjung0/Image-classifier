from PIL import Image as Img
from PIL.ExifTags import GPSTAGS
from pathlib import Path
from datetime import datetime as dt

from image_data.logic.StartPointInterface import StartPointInterface

from image_data.model import Section

GPS = 34856
DATETIME = 306

class ExtractMetaData(StartPointInterface):
    def __init__(self) -> None: pass

    def prepare(self) -> None: pass 

    def processing(self, section:Section) -> Section:

        try:
            for m in section:
                m.gps, m.datetime = self.getInfo(m.path)
        except Exception as e:
            raise e
        
        return section
    
    def getInfo(self, path:Path):
        exif = Img.open(str(path)).getexif()
        if not exif:
            return None, None
        
        gps = None
        if GPS in exif:
            gps = {}
            for t, value in GPSTAGS.items():
                if t in exif[GPS]:
                    gps[value] = exif[GPS][t]
        
        datetime = None
        if DATETIME in exif:
            datetime = dt.strptime(exif[DATETIME],"%Y:%m:%d %H:%M:%S")

        return gps, datetime
    
        

