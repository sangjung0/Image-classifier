import matplotlib.pyplot as plt
import numpy as np
import cv2

from project_constants import PROCESSOR_STOP
from video import Loader

class ImgTable:
    def __init__(self, videoLoader:Loader):
        self.__videoLoader = videoLoader

    def show(self):
        self.__videoLoader.run()
        it = iter(self.__videoLoader)
        fig, axs = plt.subplots(10, 10, figsize=(10, 10))
        idx = 0
        while True:
            flag, ret, frame = next(it)
            if ret:
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
                    face = cv2.resize(face, (width, height))

                    newFace = np.zeros((50, 50, 3), dtype=np.uint8)
                    newFace[(50-height)//2:(50-height)//2+height, (50-width)//2:(50-width)//2+width] = face

                    axs[idx//10, idx % 10].imshow(newFace)
                    axs[idx//10, idx % 10].axis('off')
                    if idx == 99: 
                        plt.draw()
                        plt.pause(0.01)

                    idx = (idx + 1) % 100

            elif flag == PROCESSOR_STOP:
                break
        self.__videoLoader.stop()
        return
