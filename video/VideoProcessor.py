from video.VideoSection import VideoSection
from multiprocessing import Queue, Value
from project_constants import STOP, PAUSE, END_OF_LOAD
import pickle
import time 

class VideoProcessor:
    def __init__(self, detector = None, tracker = None, sceneDetector = None, draw:bool = False ):
        self.__detector = detector
        self.__tracker = tracker
        self.__draw = draw
        self.__sceneDetector = sceneDetector

    def processing(self, videoSection:VideoSection):
        print(videoSection.index, "처리 시작")
        tracker = None
        if  self.__tracker is not None:
            tracker = self.__tracker.getTracker() #고민해보자
        for frame in videoSection.frameAry:
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

        print(videoSection.index, "처리 완료")
        return videoSection
    
    def __call__(self, data: Queue, result: Queue, flag: Value): # type: ignore
        while True:
            if flag.value == PAUSE:
                time.sleep(0.5)
            elif flag.value == STOP:
                break
            else:
                if not data.empty():
                    result.put(pickle.dumps(self.processing(pickle.loads(data.get()))))
                elif flag.value == END_OF_LOAD:
                    break
        print("연산 프로세서 종료")
    
class VideoProcessorGenerator:
    def __init__(self, detector, tracker, sceneDetector, draw):
        self.__detector = detector
        self.__tracker = tracker
        self.__sceneDetector = sceneDetector
        self.__draw = draw

    def generate(self):
        return VideoProcessor(self.__detector, self.__tracker, self.__sceneDetector, self.__draw)