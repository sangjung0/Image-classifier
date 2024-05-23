from threading import Lock

from program.core.scheduler.dto import Packet


class Transceiver:
    def __init__(self):
        self.__lock: Lock
        self.__data: list[object]

    def __len__(self) -> int: pass

    def append(self, value: Packet): pass

    def get(self) -> object: pass

    def is_empty(self) -> bool: pass
