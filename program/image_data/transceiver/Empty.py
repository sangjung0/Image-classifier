from multiprocessing import Queue as Q

from image_data.transceiver import Interface

from image_data.compressor import CompressorInterface
from image_data.serializer import SerializerInterface

class Empty(Interface):

    def __init__(self, source:Q, destination:Q):
        self.__source = source
        self.__destination = destination

    def send(self, value):
        self.__destination.put(value)

    def receive(self):
        if self.__source.empty():
            return False, None
        return True, self.__source.get()