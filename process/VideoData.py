import cv2

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
        self.__fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

    def __enter__(self):
        self.__cap = VideoData.read(self.fileName)
        return VideoData.__FrameIter(self.__cap)
    
    def __exit__(self):
        self.__cap.release()

    class __FrameIter:
        def __init__(self, cap:cv2.VideoCapture):
            self.__cap = cap
            self.__index = -1

        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__cap.isOpened():
                ret, frame = self.__cap.read()
                if ret:
                    self.__index += 1
                    return self.__index, frame
            raise StopIteration

    @staticmethod
    def read(fileName):
        return cv2.VideoCapture(fileName)
