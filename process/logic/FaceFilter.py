import math

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section

from project_constants import DETECTOR_FACE

class FaceFilter(StopOverPointInterface):

    def __init__(self, width:int, height:int, margin:float):
        self.__width = width
        self.__height = height
        self.__margin = margin

    def prepare(self) -> None: return

    def resize(self, lx, ly, rx, ry):
        frameWidth = self.__width
        frameHeight = self.__height
        margin = self.__margin

        widthMargin = (rx - lx) * margin/2
        heightMargin = (ry - ly)* margin/2
        lx = int(lx - widthMargin)
        ly = int(ly - heightMargin)
        rx = int(rx + widthMargin)
        ry = int(ry + heightMargin)

        width = rx - lx
        height = ry - ly

        if height > width:
            temp = (height - width)/2
            lx -= math.ceil(temp)
            rx += math.floor(temp)
        elif height < width:
            temp = (width - height)/2
            ly -= math.ceil(temp)
            ry += math.ceil(temp)

        lx = max(0, min(lx, frameWidth))
        ly = max(0, min(ly, frameHeight))
        rx = max(0, min(rx, frameWidth))
        ry = max(0, min(ry, frameHeight))

        return lx, ly, rx, ry

    def processing(self, section: Section) -> Section:

        for frame in section:
            for face in frame.face:
                face.faceData[DETECTOR_FACE] = self.resize(*face.face)
                

        return section