from util import VideoData
from util import imgFilters
from face_detector import MyMTCNN, HaarCascade
from face_tracker import LucasKanade, GunnerFarneback
from util import CalcHistogram

def readTest(fileName):
    video = VideoData(fileName)
    video.play()

def mtcnnTest(fileName):
    video = VideoData(fileName)
    mtcnn = MyMTCNN()
    video.play(mtcnn.detect)

def haarTest(fileName):
    video = VideoData(fileName)
    haar = HaarCascade()
    video.play(haar.detect)

def imgFilterTest(fileName):
    video = VideoData(fileName)
    video.play( filter = lambda x : imgFilters.bilateralFiltering(x, inplace=True))

def trackingTest(fileName):
    video = VideoData(fileName)
    tracker = LucasKanade()
    video.play( tracking= lambda x, y : tracker.tracking(x, inplace=True, isNewScene=y))

def trackingTest2(fileName):
    video = VideoData(fileName)
    tracker = GunnerFarneback()
    video.play( tracking = lambda x, y : tracker.tracking(x, inplace=True))

    
def sceneChangeTest(fileName):
    video = VideoData(fileName)
    tracker = LucasKanade()
    change = CalcHistogram()
    video.play( tracking= lambda x, y : tracker.tracking(x, inplace=True, isNewScene=y), isNewScene=change.isNewScene)