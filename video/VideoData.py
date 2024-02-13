import cv2
import numpy as np

class VideoData:    
    def __init__(self, fileName = None):
        self.fileName = fileName

    @property
    def fileName(self):
        return self.__fileName
    @fileName.setter
    def fileName(self, value):
        #Path 객체로 변경 할 것
        if isinstance(value, str) and value.strip() != '':
            self.__fileName = value
            self.setVideoMetaData()
        else: raise Exception("fileName 값 잘못 됨")

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

    # def play(self, detector = None, filter = None, tracker = None, sceneDetector = None):
    #     if(self.fileName is None): raise Exception("파일 이름 없음")

    #     cap = VideoData.read(self.fileName)
    #     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     delay = int(1000/cap.get(cv2.CAP_PROP_FPS))
    #     count = 0

    #     while(cap.isOpened()):
    #         ret, frame = cap.read()
    #         if count % self.detectFrame == 0:
    #             count = 0

    #         if ret:
    #             resizedFrame = cv2.resize(frame, (width//self.__scale, height//self.__scale))
    #             img = filter(resizedFrame) if filter is not None else resizedFrame
    #             isNewScene = sceneDetector.isNewScene(img) if sceneDetector else False

    #             if detector is not None and (count == 0 or isNewScene):
    #                 faceLocation = detector.detect(img, draw=True, drawFrame=frame)

    #             if tracker is not None:
    #                 trackingData = tracker.tracking(img, isNewScene=isNewScene, draw=True, drawFrame=frame)

    #             cv2.imshow(self.fileName, frame)
    #         count += 1

    #         if cv2.waitKey(delay) & 0xFF == ord('q'):
    #             break
    #     cap.release()
    #     cv2.destroyAllWindows()

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
            self.__cap.release()
            return StopIteration

    @staticmethod
    def read(fileName):
        return cv2.VideoCapture(fileName)
