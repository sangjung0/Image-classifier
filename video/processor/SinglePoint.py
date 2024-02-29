import os

from video.model import Section
from video.logic import StartPointInterface
from util import CompressorInterface
from util.util import Timer, Loger

class SinglePoint:
    def __init__(self, name: str, logic:StartPointInterface, compressor = CompressorInterface):
        self.__loger = Loger(name) # logger
        self.__timer = Timer() # timer
        self.__isFinish = False
        self.__logic = logic
        self.__logic.prepare()
        self.__compressor = compressor
        self.__index = 0
        self.__loger("start") # loger

    def setIsFinish(self, value):
        if isinstance(value, bool):
            self.__isFinish = value
        else:
            raise ValueError("isFinish is must be boolean")

    def get(self):
        loger = self.__loger # logger
        timer = self.__timer # timer
        try:
            if self.__isFinish:
                loger(os.getpid(), "종료", option="terminate")
                return None

            data = timer.measure(self.__logic())
            loger("데이터 연산", option=timer)
            self.__index = data.index
            videoSection = Section(self.__index, compressor=self.__compressor)
            for i in data:
                videoSection.append(i)
            return videoSection
        except Exception as e:
            loger(os.getpid(), "오류", e)
        loger(f"연산 평균 속도 {timer.average}", option='result')
        return