from typing import Type
import cv2
import numpy as np

from video.model import Section
from face_tracker import TrackerInterface
from video.processor.ProcessorInterface import ProcessorInterface

class TrackerProcessor(ProcessorInterface):
    def __init__(self, tracker: Type[TrackerInterface], scale:int, draw:bool) -> None:
        super().__init__("TrackerProcessor")
        self.__tracker = tracker
        self.__draw = draw
        self.__scale = scale
        self.__colorAry = None
        self.__lines = None

    def __prepare__(self) -> None:
        if self.__tracker is not None: 
            self.__tracker = self.__tracker()
            self.__colorAry = np.random.randint(0,255,(self.__tracker.pointNumber,3))
                
    def draw(self, points:list, frame:np.ndarray) -> None:
        scale = self.__scale
        colorAry = self.__colorAry
        lines = self.__lines
        for i, (p, n) in enumerate(points):
            px, py = map(lambda x : int(x*scale), p.ravel())
            nx, ny = map(lambda x: int(x*scale), n.ravel())
            cv2.line(lines, (px, py),(nx, ny), colorAry[i].tolist(), 2)
            cv2.circle(frame, (nx, ny), 2, colorAry[i].tolist(), -1)        
        cv2.addWeighted(frame, 1.0, lines, 1.0, 0, frame)

    def clear(self, frame:np.ndarray) -> None:
        self.__lines = np.zeros_like(frame)

    def processing(self, section:Section) -> Section:
        tracker = self.__tracker
        draw = self.__draw

        if tracker is None: return section

        for frame in section:
            points = tracker.tracking(frame.getFrame(tracker.colorConstant), frame.isNewScene)
            if draw:
                if len(points) == 0:
                    self.clear(frame.frame) #만약 그리는게 이상하면 이거 수정
                else:
                    self.draw(points, frame.frame)
            section.compress(frame)
        return section

