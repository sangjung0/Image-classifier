from multiprocessing import Queue, Value
import os
import time
from typing import Type

from util.transceiver import TransceiverInterface
from video.VideoData import VideoData
from video.model import Frame, VideoSection
from project_constants import PAUSE, STOP, RUN, END_OF_LOAD

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

            with self.__videoData as v:
                it = iter(v)
                while True:
                    if flag.value == RUN:
                        if videoSectionIndex - lastIndex.value < 5:
                            try:
                                index, frame = next(it)
                                videoSection.append(self.__frameGenerator(index, frame))
                                if len(videoSection) >= self.__cfl:
                                    transceiver.send(data, videoSection)
                                    print(videoSectionIndex, "보냄")
                                    videoSectionIndex += 1
                                    videoSection.clear(videoSectionIndex)
                                    time.sleep(0.1)
                            except StopIteration:
                                break
                    elif flag.value == STOP:
                        print(os.getpid(),"영상 로드 프로세서 종료")
                        return
                    elif flag.value == PAUSE:
                        time.sleep(0.1)
        except Exception as e:
            print(os.getpid(), "영상 분배기 오류", e)
            
        print(os.getpid(), "영상 분배기 종료")
        flag.value = END_OF_LOAD
        return
