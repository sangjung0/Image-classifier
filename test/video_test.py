from util import VideoData
from util import imgFilters
from face_detector import MyMTCNN, HaarCascade, FaceDetectorFilter
from face_tracker import LucasKanade, GunnerFarneback
from util import CalcHistogram, CalcEdge

def readTest(fileName, scale):
    video = VideoData(fileName)
    video.play()

def mtcnnTest(fileName, scale):
    video = VideoData(fileName, scale=scale)
    faceDetectorFilter = FaceDetectorFilter(MyMTCNN(), scale = scale)
    video.play(detector = faceDetectorFilter)

def haarTest(fileName, scale):
    video = VideoData(fileName, scale=scale)
    faceDetectorFilter = FaceDetectorFilter(HaarCascade(), scale = scale)
    video.play(detector = faceDetectorFilter)

def imgFilterTest(fileName, scale):
    video = VideoData(fileName, scale=scale)
    video.play( filter = imgFilters.bilateralFiltering)

def trackingTest(fileName, scale):
    video = VideoData(fileName, scale=scale)
    tracker = LucasKanade(scale=scale)
    video.play( tracker= tracker)

def trackingTest2(fileName, scale):
    pass
#     video = VideoData(fileName)
#     tracker = GunnerFarneback()
#     video.play( tracker = tracker)

    
def sceneChangeTest(fileName, scale):
    video = VideoData(fileName, scale=scale)
    tracker = LucasKanade(scale=scale)
    video.play( tracker= tracker, sceneDetector=CalcHistogram())

def sceneChangeTest2(fileName, scale):
    video = VideoData(fileName, scale=scale)
    tracker = LucasKanade(scale=scale)
    video.play( tracker= tracker, sceneDetector=CalcEdge())