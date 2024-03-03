import numpy as np
import cv2

from project_constants import PROCESSOR_STOP
from video import Loader
from util.util import Loger

class ExtractFace:
    def __init__(self, videoLoader:Loader):
        self.__videoLoader = videoLoader

    def extract(self):
        self.__videoLoader.run()
        loger = Loger("ExtractFace")
        loger("start")

        idx = 0
        all_images = []
        for flag, ret, frame in self.__videoLoader:
            if ret:
                if idx % 100 == 0:
                    loger(f"{idx} 완료")
                for face in frame.face:
                    lx, ly, rx, ry = face.face
                    face = frame.frame[ly:ry, lx:rx]
                    width = rx - lx
                    height = ry - ly
                    if height > width:
                        width = int(50 * width / height)
                        height = 50
                    else:
                        height = int(50 * height / width)
                        width = 50
                    face = cv2.cvtColor(cv2.resize(face, (width, height)), cv2.COLOR_BGR2RGB)

                    newFace = np.zeros((50, 50, 3), dtype=np.uint8)
                    newFace[(50-height)//2:(50-height)//2+height, (50-width)//2:(50-width)//2+width] = face

                    all_images.append(newFace)
                idx+=1
            elif flag == PROCESSOR_STOP:
                break
        loger(f"완료. {len(all_images)}",  option="terminate")
        all_images = np.array(all_images, dtype=np.uint8)
        return all_images
