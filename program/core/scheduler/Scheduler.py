import pathlib
from collections import deque


class Scheduler:
    def __init__(self):
        self.__queue: deque

    def add(self, path: pathlib.Path): pass

    def peek(self, n: int) -> pathlib.Path: pass

    def poll(self, n: int) -> pathlib.Path: pass

    def is_empty(self) -> bool: pass

    def run(self): pass
