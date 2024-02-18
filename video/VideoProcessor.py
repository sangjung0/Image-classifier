from multiprocessing import Queue, Value
import os
import time

from video.model import VideoSection
from util.transceiver import TransceiverInterface
from project_constants import STOP, PAUSE, END_OF_LOAD
from util.util import Timer, Loger

class VideoProcessor:
    def __init__(self, detector, tracker, sceneDetector, draw:bool):
        self.__detector = detector
        self.__tracker = tracker
        self.__draw = draw
        self.__sceneDetector = sceneDetector

    def processing(self, videoSection:VideoSection):
        tracker = None
        if  self.__tracker is not None:
            tracker = self.__tracker.getTracker() #고민해보자
        for idx, frame in enumerate(videoSection):
            isNewScene = False if self.__sceneDetector is None else self.__sceneDetector.isNewScene(frame.getFrame())
            if frame.isDetect or isNewScene:
                if self.__detector is not None:
                    faceLocation = self.__detector.detect(frame.getFrame(self.__detector.colorConstant), self.__draw, frame.frame, frame.scale)
            #     if tracker is not None:
            #         trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), True, self.__draw, frame.frame, frame.scale)
            # else:
            #     if tracker is not None:
            #         trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), False, self.__draw, frame.frame, frame.scale)
            
            if tracker is not None:
                trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), isNewScene, self.__draw, frame.frame, frame.scale)
            videoSection.compress(idx)
        return videoSection
    
    def __call__(self, data: Queue, result: Queue, flag: Value, transceiver:TransceiverInterface): # type: ignore
        try:
            timer = Timer() # timer
            loger = Loger("VideoProcessor") # logger
            while True:
                if flag.value == PAUSE:
                    time.sleep(0.1)
                elif flag.value == STOP:
                    break
                else:
                    if not data.empty():
                        timer.start() # timer
                        ret, data_ = transceiver.receive(data)
                        timer.end() # timer
                        loger("데이터 수신 후 압축 해제", timer=timer) # loger
                        if ret:
                            timer.start() # timer
                            temp = self.processing(data_)
                            timer.end() # timer
                            loger("데이터 연산 완료", timer=timer) # loger
                            timer.start() # timer
                            transceiver.send(result, temp)
                            timer.end() # timer
                            loger("데이터 압축 후 전송", timer=timer) # loger
                        elif flag.value == END_OF_LOAD:
                            break
                    time.sleep(0.1)
            loger(os.getpid(), "연산 프로세서 종료")
        except Exception as e:
            loger(os.getpid(), "연산 프로세서 오류", e)
        return
    
class VideoProcessorGenerator:
    def __init__(self, detector, tracker, sceneDetector, draw):
        self.__detector = detector
        self.__tracker = tracker
        self.__sceneDetector = sceneDetector
        self.__draw = draw

    def generate(self):
        return VideoProcessor(self.__detector, self.__tracker, self.__sceneDetector, self.__draw)