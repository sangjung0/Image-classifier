import cv2
import numpy as np

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section

class TraceLineVisualizer(StopOverPointInterface):
    def __init__(self, pointNumber:int) -> None:
        self.__pointNumber = pointNumber
        self.__colorAry = None
        self.__lines = None

    def prepare(self) -> None:
        self.__colorAry = np.random.randint(0,255,(self.__pointNumber,3))
                
    def draw(self, prevPt:list, nextPt:list, frame:np.ndarray) -> None:
        colorAry = self.__colorAry
        lines = self.__lines
        for i, (p, n) in enumerate(zip(prevPt, nextPt)):
            px, py = p
            nx, ny = n
            cv2.line(lines, (px, py),(nx, ny), colorAry[i].tolist(), 2)
            cv2.circle(frame, (nx, ny), 2, colorAry[i].tolist(), -1)        
        cv2.addWeighted(frame, 1.0, lines, 1.0, 0, frame)

    def clear(self, frame:np.ndarray) -> None:
        self.__lines = np.zeros_like(frame)

    def processing(self, section:Section) -> Section:

        for frame in section:
            prevPt, nextPt = frame.points
            if prevPt is None or frame.isNewScene: self.clear(frame.frame)
            else: self.draw(prevPt, nextPt, frame.frame)

        return section

