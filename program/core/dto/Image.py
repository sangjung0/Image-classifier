import pathlib
import datetime
import PIL
import PIL.Image
from PIL.ExifTags import TAGS
import numpy as np

from core.dto.Character import Character


class Image:
    """
    이미지 정보를 가지고 있음
    이미지 경로, 이름, 날짜, 시간, 등장인물, 해시 값 등의 메타데이터와 이미지 자체 데이터
    """
    def __init__(self, path: pathlib.Path):
        self.__path: pathlib.Path = path
        self.__date: datetime.datetime = None
        self.__time: datetime.time = None

        self.__histogram: np.ndarray = None
        self.__is_detected: bool = False
        
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
            with PIL.Image.open(self.__path) as img:
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
                
    def __set_data(self):
        """
        이미지 메타데이터 읽은 후 매개변수 초기화
        """
        
        with PIL.Image.open(self.__path) as img:
            exif_data = img.getexif()
            
            if exif_data is not None:
                exif = {
                    TAGS.get(tag): value
                    for tag, value in exif_data.items()
                    if tag in TAGS
                }
                
                date_time_str = exif.get('DateTime', 'N/A')
                
                if date_time_str != 'N/A':
                    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y:%m:%d %H:%M:%S')
                    self.__date = date_time_obj.date()
                    self.__time = date_time_obj.time()

