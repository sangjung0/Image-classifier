from multiprocessing import Queue, Value

from video.model import VideoSection
from util.transceiver import TransceiverInterface
from project_constants import STOP, PAUSE, END_OF_LOAD

class VideoProcessor:
    def __init__(self, detector, tracker, sceneDetector, draw:bool):
        self.__detector = detector
        self.__tracker = tracker
        self.__draw = draw
        self.__sceneDetector = sceneDetector

    def processing(self, videoSection:VideoSection):
        print(videoSection.index, "처리 시작")
        tracker = None
        if  self.__tracker is not None:
            tracker = self.__tracker.getTracker() #고민해보자
        for frame in videoSection.frames:
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
    
    def __call__(self, data: Queue, result: Queue, flag: Value, transceiver:TransceiverInterface): # type: ignore
        while True:
            if flag.value == PAUSE:
                pass
            elif flag.value == STOP:
                break
            else:
                ret, data_ = transceiver.receive(data)
                if ret:
                    transceiver.send(result, (self.processing(data_)))
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