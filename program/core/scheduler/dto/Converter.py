from multiprocessing import Queue
import numpy as np
from PIL import Image
import io

from core.scheduler.dto.Packet import Packet


class Converter:
    """
    데이터 조작 및 전송하는 클래스
    데이터 송신 전 PacketData의 이미지를 손실 압축
    데이터 수신 후 PacketData의 이미지를 압축 해제 하는 역할.
    """
    __TIMEOUT:int = 1
    
    def __init__(self, source: Queue) -> None:
        self.__source: Queue = source
        
    def __compress(self, value:np.ndarray) -> bytes:
        if value is None: return None
        byteIo = io.BytesIO()
        Image.fromarray(value).save(byteIo, format='JPEG')
        return byteIo.getvalue()
    
    def __decompress(self, value:bytes) -> np.ndarray:
        if value is None: return None
        return np.array(Image.open(io.BytesIO(value)))
        
    def send(self, value: Packet) -> None:
        for i in value: i.image = (self.__compress(i.image))
        self.__source.put(value)

    def receive(self) -> tuple[bool, Packet]:
        value = self.__source.get(timeout=Converter.__TIMEOUT)
        for i in value: i.image = (self.__decompress(i.image))
        return True, value
        