import pathlib
import datetime
from PIL import Image as IMG
from PIL.ExifTags import TAGS, GPSTAGS
import numpy as np

from core.dto.Character import Character
from core.ReverseGeocoder import ReverseGeocoder


class Image:
    """
    이미지 정보를 가지고 있음
    이미지 경로, 이름, 날짜, 시간, 등장인물, 해시 값 등의 메타데이터와 이미지 자체 데이터
    """
    
    __DATETIME:str = "DateTime"
    __GPS_INFO:str = "GPSInfo"
    __GPS_LATITUDE:str = "GPSLatitude"
    __GPS_LATITUDE_REF:str = "GPSLatitudeRef"
    __GPS_LONGITUDE:str = "GPSLongitude"
    __GPS_LONGITUDE_REF:str = "GPSLongitudeRef"
    __STR_TO_DATE:str = '%Y:%m:%d %H:%M:%S'
    
    def __init__(self, path: pathlib.Path):
        self.__path: pathlib.Path = path
        self.__date: datetime.datetime = None
        self.__time: datetime.time = None
        
        self.latitude = None
        self.longitude = None
        self.location = None

        self.__histogram: np.ndarray = None
        self.is_detected: bool = False
        self.is_scheduled: bool = False
        
        self.characters: dict[int: Character] = {}
        
        self.__set_data()
        
    @property
    def path(self) -> pathlib.Path:
        return self.__path
    
    @property
    def name(self) -> str:
        return self.__path.name
    
    @property
    def date(self) -> datetime.datetime:
        return self.__date
    
    @property
    def time(self) -> datetime.time:
        return self.__time
    
    @property
    def histogram(self) -> np.ndarray:
        return self.__histogram
    
    @histogram.setter
    def histogram(self, value:np.ndarray) -> None:
        if isinstance(value, np.ndarray):
            self.__histogram = value
        else: raise TypeError()
    
    @property
    def image(self) -> np.ndarray:
        try:
            with IMG.open(self.__path) as img:
                image = img.convert('RGB')
                return np.array(image, dtype=np.uint8)
        except Exception as _:
            return None
        
    @property
    def is_detected(self) -> bool:
        return self.__is_detected
    
    @is_detected.setter
    def is_detected(self, value:bool):
        if isinstance(value, bool):
            self.__is_detected = value
        else: raise TypeError()
        
    @property
    def is_scheduled(self) -> bool:
        return self.__is_scheduled
    @is_scheduled.setter
    def is_scheduled(self, value:bool):
        if isinstance(value, bool):
            self.__is_scheduled = value
        else: raise TypeError()
                
    def __set_data(self):
        """
        이미지 메타데이터 읽은 후 매개변수 초기화
        """
        
        with IMG.open(self.__path) as img:
            exif_data = img.getexif()
            
            if exif_data is not None:
                exif = {}
                
                for tag, value in exif_data.items():
                    if tag in TAGS: exif[TAGS[tag]] = value
                    
                if Image.__DATETIME in exif:
                    date_time_obj = datetime.datetime.strptime(exif[Image.__DATETIME], Image.__STR_TO_DATE)
                    self.__date = date_time_obj.date()
                    self.__time = date_time_obj.time()
                    
                # GPS 정보 추출
                if Image.__GPS_INFO in exif:
                    gps_data = {}
                    
                    for tag, value in exif[Image.__GPS_INFO].items():
                        if tag in GPSTAGS: gps_data[GPSTAGS[tag]] = value
                        
                    self.latitude = ReverseGeocoder.convert_gps_data(gps_data[Image.__GPS_LATITUDE], gps_data[Image.__GPS_LATITUDE_REF])
                    self.longitude = ReverseGeocoder.convert_gps_data(gps_data[Image.__GPS_LONGITUDE], gps_data[Image.__GPS_LONGITUDE_REF])
                    self.location = ReverseGeocoder.get_location_name(self.latitude, self.longitude)
