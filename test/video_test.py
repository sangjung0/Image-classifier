from video import VideoPlayer
from util import imgFilters
from face_detector import MyMTCNN, HaarCascade, FaceDetectorFilter
from face_tracker import LucasKanade, GunnerFarneback
from util import CalcHistogram, CalcEdge

def readTest(fileName):
    video = VideoPlayer(fileName)
    video.singleProcessPlay()

def mtcnnTest(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, detector=FaceDetectorFilter(MyMTCNN()))
    video.singleProcessPlay()

def haarTest(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, detector=FaceDetectorFilter(HaarCascade()))
    video.singleProcessPlay()

def imgFilterTest(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, filter = imgFilters.bilateralFiltering)
    video.singleProcessPlay()

def trackingTest(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade())
    video.singleProcessPlay()

def trackingTest2(fileName, scale):
    pass
#     video = VideoData(fileName)
#     tracker = GunnerFarneback()
#     video.play( tracker = tracker)

    
def sceneChangeTest(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), sceneDetector=CalcHistogram())
    video.singleProcessPlay()

def sceneChangeTest2(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), sceneDetector=CalcEdge())
    video.singleProcessPlay()

def test1(fileName, scale):
    video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), filter=imgFilters.gaussianFiltering)
    video.singleProcessPlay(  )
    # haar은 명암을 통해서 얼굴 인식하니까 명암비 조작이 더 좋을지도