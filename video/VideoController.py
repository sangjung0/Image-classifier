from video.VideoBuffer import VideoBuffer
from video.VideoData import VideoData
from video.Frame import FrameGenerator
from video.VideoLoader import VideoLoader
from video.VideoProcessor import VideoProcessorGenerator
from multiprocessing import Process, Queue, Value
from project_constants import STOP, RUN, PAUSE, END_OF_LOAD
from threading import Thread
import pickle
import time

from video.VideoSection import VideoSection

class VideoController:
    def __init__(self, fileName:str, detectFrameCount:int = 1, scale:int = 1, cfl:int = 100, filter = None, detector = None, tracker = None, sceneDetector = None, draw:bool = False ) -> None:
        self.__videoData = VideoData(fileName)

        self.frameGenerator = FrameGenerator(
            self.__videoData.width, self.__videoData.height, scale, filter,
            lambda x: x % detectFrameCount == 0, 
        ).generate

        self.videoProcessorGenerator = VideoProcessorGenerator(detector, tracker, sceneDetector, draw).generate
        self.__cfl = cfl

        self.data = Queue()
        self.result = Queue()
        self.flag = Value('i',PAUSE)
        self.processes = []


    @property
    def videoData(self):
        return self.__videoData

    def getVideoLoader(self, processorNumber = 1):

        videoBuffer = VideoBuffer()
        processes = []

        Process(target=self.videoDistributor).start()
        for _ in range(processorNumber):
            p = Process(target=self.videoProcessorGenerator(), args=(self.data, self.result, self.flag))
            p.start()
            processes.append(p)
        Thread(target=videoBuffer, args=(self.result, self.flag, lambda : not any(p.is_alive() for p in processes))).start()

        return VideoLoader(videoBuffer, self.flag)
    

    def videoDistributor(self): # type: ignore
        frameAry = []
        videoSectionIndex = 0

        with self.__videoData as v:
            it = iter(v)
            while True:
                if self.flag.value == RUN:
                    try:
                        index, frame = next(it)
                        frameAry.append(self.frameGenerator(index, frame))
                        if len(frameAry) >= self.__cfl:
                            self.data.put(pickle.dumps(VideoSection(videoSectionIndex, frameAry)))
                            frameAry.clear()
                            print(videoSectionIndex, "보냄")
                            videoSectionIndex += 1
                    except StopIteration:
                        break
                elif self.flag.value == PAUSE:
                    time.sleep(0.5)
                elif self.flag.value == STOP:
                    break
        print("영상 로드 프로세서 종료")
        self.flag.value = END_OF_LOAD