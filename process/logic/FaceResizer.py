import math

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section

from project_constants import DETECTOR_FACE

class FaceResizer(StopOverPointInterface):

    def __init__(self, margin:float):
        self.__margin = margin

    def prepare(self): return

    def resize(self, imgWidth, imgHeight, lx, ly, rx, ry) -> tuple[int, int, int, int]:
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

        lx = max(0, min(lx, imgWidth))
        ly = max(0, min(ly, imgHeight))
        rx = max(0, min(rx, imgWidth))
        ry = max(0, min(ry, imgHeight))

        return lx, ly, rx, ry

    def processing(self, section: Section) -> Section:

        for img in section:
            for face in img.face:
                face.faceData[DETECTOR_FACE] = self.resize(img.width, img.height, *face.face)
                
        return section