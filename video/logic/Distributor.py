from video.model import Frame, Section
from video.VideoData import VideoData
from video.logic.StartPointInterface import StartPointInterface

class Distributor(StartPointInterface):
    def __init__(self, videoData:VideoData, detectFrameCount:int, cfl:int):
        self.__videoData = videoData
        self.__cfl = cfl
        self.__detectFrameCount = detectFrameCount
        self.__iter = None
        self.__setIsFinish = None
        self.__index = 0

    def prepare(self, setIsFinish:callable) -> None:
        self.__isDetect = lambda x: x % self.__detectFrameCount == 0
        self.__iter = self.__videoData.__enter__()
        self.__setIsFinish = setIsFinish

    def processing(self, section:Section) -> Section:
        it = self.__iter
        self.__index += 1
        isDetect = self.__isDetect
        cfl = self.__cfl
        try:
            while True:
                index, frame = next(it)
                section.append(Frame(index, frame, isDetect(index % cfl)))
                if len(section) >= cfl:
                    break
        except StopIteration:
            self.__setIsFinish(True)
            self.__videoData.__exit__()
        except Exception as e:
            self.__videoData.__exit__()
            raise e
        return section