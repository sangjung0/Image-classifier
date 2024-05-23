from multiprocessing import Queue

from program.core.scheduler.dto.Packet import Packet


class Converter:
    def __init__(self, source: Queue):
        self.__source: Queue

    def send(self, value: Packet): pass

    def receive(self) -> Packet: pass
