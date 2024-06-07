from threading import Lock
from collections import deque

from core.scheduler.dto import Packet


class Transceiver:
    def __init__(self) ->None:
        self.__lock: Lock = Lock()
        self.__data: deque[Packet] = deque()

    def __len__(self) -> int:
        return len(self.__data)

    def append(self, value: Packet) ->None:
        with self.__lock:
            self.__data.append(value)

    def get(self) -> object:
        if self.is_empty(): return None
        with self.__lock:
            return self.__data.popleft()

    def is_empty(self) -> bool:
        return len(self.__data) == 0
