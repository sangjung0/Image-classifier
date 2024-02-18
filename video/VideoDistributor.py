from multiprocessing import Queue, Value
import os
import time
from typing import Type

from util.transceiver import TransceiverInterface
from video.VideoData import VideoData
from video.model import Frame, VideoSection
from project_constants import PAUSE, STOP, RUN, END_OF_LOAD
from util.util import Loger, Timer

class VideoDistributor:
    def __init__(self, videoData:VideoData, scale:int, detectFrameCount:int, cfl:int, filter:Type[object]):
        self.__videoData = videoData
        self.__cfl = cfl
        self.__frameGenerator = Frame.FrameGenerator(
            videoData.width, videoData.height, scale, filter,
            lambda x: x % detectFrameCount == 0, 
        ).generate


    def __call__(self, data: Queue, flag: Value, lastIndex: Value, transceiver:TransceiverInterface): # type: ignore
        try:
            videoSectionIndex = 0
            videoSection = VideoSection(videoSectionIndex)

            loger = Loger("VideoDistributor") # loger
            timer = Timer() # timer
            timer.start() # timer

            with self.__videoData as v:
                it = iter(v)
                while True:
                    if flag.value == RUN:
                        if videoSectionIndex - lastIndex.value < 5:
                            try:
                                index, frame = next(it)
                                videoSection.append(self.__frameGenerator(index, frame))
                                if len(videoSection) >= self.__cfl:
                                    timer.end() # timer
                                    loger("videoSection 데이터 담기", timer=timer) # loger
                                    timer.start() # timer
                                    transceiver.send(data, videoSection)
                                    timer.end() # timer
                                    loger(videoSectionIndex, "압축 후 보냄", timer=timer) # loger
                                    
                                    videoSectionIndex += 1
                                    videoSection.clear(videoSectionIndex)
                                    time.sleep(0.1)
                                    timer.start() # timer
                            except StopIteration:
                                break
                    elif flag.value == STOP:
                        loger(os.getpid(),"영상 로드 프로세서 종료") # loger
                        return
                    elif flag.value == PAUSE:
                        time.sleep(0.1)
        except Exception as e:
            loger(os.getpid(), "영상 분배기 오류", e) # loger
            
        loger(os.getpid(), "영상 분배기 종료") # loger
        flag.value = END_OF_LOAD
        return
