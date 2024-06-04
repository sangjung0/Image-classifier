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
        self.__name: str = path.name

        self.__img: PIL.Image.Image = None
        self.__date: datetime.datetime = None
        self.__time: datetime.time = None
        self.__characters: list[Character] = None
        self.__hash: bin = None
        self.__is_detected: bool = False
        
        self.__set_data()
        
    def __set_data(self):
        """
        이미지 메타데이터 읽은 후 매개변수 초기화
        """
        self.__img = PIL.Image.open(self.__path)
        exif_data = self.__img.getexif()
        
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
        

    def get_path(self) -> pathlib.Path:
        return self.__path

    def get_name(self) -> str:
        return self.__name

    def get_date(self) -> datetime.datetime:
        return self.__date

    def get_time(self) -> datetime.time:
        return self.__time

    def get_characters(self) -> tuple[Character]:
        return self.__characters

    def get_hash(self) -> bin:
        return self.__hash

    def get_image(self) -> np.ndarray:
        return np.array(self.__img)

    def is_detected(self) -> bool:
        return self.__is_detected

    def set_characters(self, characters: list[Character]):
        self.__characters.append(*characters)

    def set_is_detected(self, b: bool):
        self.__is_detected = b

    def set_hash(self, _hash: bin):
        self.__hash = _hash
