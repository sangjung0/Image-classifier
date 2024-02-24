import numpy as np
import cv2

from project_constants import PROCESSOR_STOP
from video import Loader
from util.util import Loger

class SaveImg:
    def __init__(self, videoLoader:Loader):
        self.__videoLoader = videoLoader

    def save(self):
        self.__videoLoader.run()
        it = iter(self.__videoLoader)
        loger = Loger("SaveImg")
        loger("start")
        idx = 0
        all_images = []
        while True:
            flag, ret, frame = next(it)
            if idx >= 20000: break
            if ret:
                if idx % 100 == 0:
                    loger(f"{idx} 완료")
                for lx, ly, rx, ry in frame.face:
                    if lx < 0: lx = 0
                    if ly < 0: ly = 0
                    if rx < 0: rx = 0
                    if ry < 0: ry = 0
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

                    cv2.imshow("tt",newFace)
                    all_images.append(newFace)

                idx+=1
            elif flag == PROCESSOR_STOP:
                break
        cv2.destroyAllWindows()
        all_images = np.array(all_images, dtype=np.uint8)
        self.__videoLoader.stop()
        np.save("test.npz", all_images)
        return
