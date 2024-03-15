import cv2
import numpy as np

from process.Loader import Loader

from project_constants import PROCESSOR_STOP

class VideoPlayer:
    def __init__(self, Loader:Loader, delay:int=2000):
        self.__loader = Loader
        self.__delay = delay

    def play(self):
        self.__loader.run()
        name = str(self.__loader.data.path)
        delay = self.__delay 
        print("딜레이 :", delay)
        for flag, ret, frame in self.__loader:
            tempDelay = 1
            if ret:
                if frame.face: tempDelay = delay
                cv2.imshow(str(name), self.background(frame))
                #cv2.imshow(str(name), cv2.resize(frame.source, (800,800)))
            elif flag == PROCESSOR_STOP: # Stop 처리는 안해도 될 듯
                break
                
            if cv2.waitKey(tempDelay) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.__loader.stop()
        return
    
    def background(self, img):
        background = np.zeros((800,800,3), dtype=np.uint8)
        height = img.height
        width = img.width

        if height > width:
            width = int(width/height * 800)
            height = 800
        else:
            height = int(height/width*800)
            width = 800

        background[0:height, 0:width] = cv2.resize(img.source,(width,height))
        return background