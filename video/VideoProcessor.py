from video.VideoSection import VideoSection

class VideoProcessor:
    def __init__(self, videoSection:VideoSection, detector = None, tracker = None, draw:bool = False, sceneDetector = None ):
        self.videoSection = videoSection
        self.__detector = detector
        self.__tracker = tracker
        self.__draw = draw
        self.__sceneDetector = sceneDetector

    @property
    def videoSection(self):
        return self.__videoSection
    @videoSection.setter
    def videoSection(self, value):
        if isinstance(value,VideoSection):
            self.__videoSection = value
        else: raise ValueError("Video section must be VideoSection")

    def processing(self):
        tracker = None
        if  self.__tracker is not None:
            tracker = self.__tracker.getTracker() #고민해보자
        for frame in self.__videoSection.frameAry:
            isNewScene = False if self.__sceneDetector is None else self.__sceneDetector.isNewScene(frame.getFrame())
            if frame.isDetect or isNewScene:
                if self.__detector is not None:
                    faceLocation = self.__detector.detect(frame.getFrame(self.__detector.colorConstant), self.__draw, frame.frame, frame.scale)
            #     if tracker is not None:
            #         trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), True, self.__draw, frame.frame, frame.scale)
            # else:
            #     if tracker is not None:
            #         trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), False, self.__draw, frame.frame, frame.scale)
            
            if tracker is not None:
                trackingData = tracker.tracking(frame.getFrame(self.__tracker.colorConstant), isNewScene, self.__draw, frame.frame, frame.scale)

        return self.__videoSection