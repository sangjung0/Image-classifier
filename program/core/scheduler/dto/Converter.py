from multiprocessing import Queue
import numpy as np
from PIL import Image
import io

from program.core.scheduler.dto.Packet import Packet


class Converter:
    """
    데이터 조작 및 전송하는 클래스
    데이터 송신 전 PacketData의 이미지를 손실 압축
    데이터 수신 후 PacketData의 이미지를 압축 해제 하는 역할.
    """
    def __init__(self, source: Queue) -> None:
        self.__source: Queue = source
        
    def __compress(self, value:np.ndarray) -> bytes:
        byteIo = io.BytesIO()
        Image.fromarray(value).save(byteIo, format='JPEG')
        return byteIo.getvalue()
    
    def __decompress(self, value:bytes) -> np.ndarray:
        return np.array(Image.open(io.BytesIO(value)))
        
    def send(self, value: Packet) -> None:
        for i in value: i.set_image(self.__compress(i.get_image()))
        self.__source.put(value)

    def receive(self) -> tuple[bool, Packet]:
        if self.__source.empty():
            return False, None
        value = self.__source.get()
        for i in value: i.set_image(self.__decompress(i.get_image()))
        return True, value
        