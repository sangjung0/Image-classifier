from multiprocessing import Queue, Value
import os
import time
from typing import Type

from util import CompressorInterface
from util import TransceiverInterface
from video.VideoData import VideoData
from video.model import Frame, Section
from project_constants import PROCESSOR_PAUSE, PROCESSOR_STOP, PROCESSOR_RUN
from util.util import Loger, Timer, DetectFrame

class Distributor:
    def __init__(self, videoData:VideoData, detectFrameCount:int, cfl:int, bufSize:int):
        self.__videoData = videoData
        self.__cfl = cfl
        self.__bufSize = bufSize
        self.__detectFrameCount = detectFrameCount

    def __call__(self, data: Queue, flag: Value, lastIndex: Value, transceiver:TransceiverInterface, compressor: Type[CompressorInterface]): # type: ignore
        loger = Loger("VideoDistributor") # loger
        try:
            #Frame
            isDetect =  DetectFrame(self.__detectFrameCount).isDetect

            #VideoSection
            videoSection = Section(0, compressor=compressor())

            loger(option="start") # loger
            timer = Timer() # timer
            timer.start() # timer

            with self.__videoData as v:
                it = iter(v)
                while True:
                    if flag.value == PROCESSOR_RUN:
                        if videoSection.index - lastIndex.value < self.__bufSize:
                            try:
                                index, frame = next(it)
                                videoSection.append(Frame(index, frame, isDetect))
                                if len(videoSection) >= self.__cfl:
                                    timer.end() # timer
                                    loger("videoSection 데이터 담기", option=timer) # loger
                                    timer.start() # timer
                                    transceiver.send(data, videoSection)
                                    timer.end() # timer
                                    loger(videoSection.index, "압축 후 보냄", option=timer) # loger
                                  
                                    videoSection.next()
                                    timer.start() # timer
                            except StopIteration:
                                break
                        else:
                            time.sleep(0.01)
                    elif flag.value == PROCESSOR_STOP:
                        break
                    elif flag.value == PROCESSOR_PAUSE:
                        time.sleep(0.1)
        except Exception as e:
            loger(os.getpid(), "영상 분배기 오류", e) # loger
            flag.value = PROCESSOR_STOP
            
        loger(os.getpid(), "영상 분배기 종료", option="terminate") # loger
        return
