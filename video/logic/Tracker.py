from typing import Type
from face_tracker import TrackerInterface
from video.model import Section, Face
from video.logic import StopOverPointInterface

class Tracker(StopOverPointInterface): #일반 트래커하고 얼굴 트래커하고 나눠보자
    def __init__(self, tracker: Type[TrackerInterface], scale:int) -> None:
        self.__tracker = tracker
        self.__scale = scale

    def prepare(self) -> None:
        self.__tracker = self.__tracker()

    def processing(self, section:Section) -> Section:
        tracker = self.__tracker
        scale = self.__scale

        for frame in section:
            prevPt, nextPt = tracker.tracking(frame.getFrame(tracker.colorConstant), frame.isNewScene)
            if nextPt is not None:
                nextPt = list(map(lambda x: tuple(int(x*scale) for x in x.ravel()), nextPt))
                if prevPt is not None:
                    prevPt = list(map(lambda x: tuple(int(x*scale) for x in x.ravel()), prevPt))
            frame.points = (prevPt, nextPt)
        return section
