from multiprocessing import Queue as Q

from image_data.transceiver.Interface import Interface

from image_data.compressor import Interface as CI
from image_data.serializer import Interface as SI
from image_data.model import Section

class Queue(Interface):

    def __init__(self, source:Q, serializer:SI, compressor: CI):
        self.__source = source
        self.__compressor = compressor
        self.__serializer = serializer
 
    def send(self,value: Section) -> None:
        self.__source.put(self.__compressor.compress(self.__serializer.serialization(value)))

    def receive(self) -> Section:
        if self.__source.empty():
            return False, None
        return True, self.__serializer.deSerialization(self.__compressor.decompress(self.__source.get()))