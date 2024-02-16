import cv2
import numpy as np

class VideoData:    
    def __init__(self, fileName):
        self.__fileName = fileName
        self.setVideoMetaData()

    @property
    def fileName(self):
        return self.__fileName
    @property
    def width(self):
        return self.__width
    @property
    def height(self):
        return self.__height
    @property
    def fps(self):
        return self.__fps

    def setVideoMetaData(self):
        cap = VideoData.read(self.fileName)
        self.__width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__fps = int(1000/cap.get(cv2.CAP_PROP_FPS))
        cap.release()

    def __enter__(self):
        self.__cap = VideoData.read(self.fileName)
        return VideoData.__FrameIter(self.__cap, self.width, self.height)
    
    def __exit__(self, exc_type, exc_value, trace):
        self.__cap.release()

    class __FrameIter:
        def __init__(self, cap:cv2.VideoCapture, width:int, height:int):
            self.__cap = cap
            self.__index = -1
            self.__prevFrame = np.zeros((width, height, 1))

        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__cap.isOpened():
                ret, frame = self.__cap.read()
                frame = frame if ret else self.__prevFrame
                self.__prevFrame = frame
                self.__index += 1
                return self.__index, frame
            #self.__cap.release()
            return StopIteration

    @staticmethod
    def read(fileName):
        return cv2.VideoCapture(fileName)
