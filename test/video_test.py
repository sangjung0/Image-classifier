from video import Controller, VideoPlayer
from imageProcessor import blurFilters, deblurFilters
from face_detector import MyMTCNN, HaarCascade
from face_tracker import LucasKanade, GunnerFarneback
from util import CalcHistogram, CalcEdge
from util import Transceiver, GZipCompressor, PickleSerializer, JpgCompressor


# def readTest(fileName):
#     video = VideoPlayer(fileName)
#     video.singleProcessPlay()

# def mtcnnTest(fileName, scale):
#     video = VideoPlayer(fileName, scale=scale, detector=FaceDetectorFilter(MyMTCNN()))
#     video.singleProcessPlay()

# def haarTest(fileName, scale):
#     video = VideoPlayer(fileName, scale=scale, detector=FaceDetectorFilter(HaarCascade()))
#     video.singleProcessPlay()

# def imgFilterTest(fileName, scale):
#     #video = VideoPlayer(fileName, scale=scale, filter = blurFilters.meanFiltering)
#     video = VideoPlayer(fileName, scale=scale, filter = deblurFilters.wienerFiltering)
#     video.singleProcessPlay()

# def trackingTest(fileName, scale):
#     video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade())
#     video.singleProcessPlay()

# def trackingTest2(fileName, scale):
#     pass
# #     video = VideoData(fileName)
# #     tracker = GunnerFarneback()
# #     video.play( tracker = tracker)

    
# def sceneChangeTest(fileName, scale):
#     video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), sceneDetector=CalcHistogram())
#     video.singleProcessPlay()

# def sceneChangeTest2(fileName, scale):
#     video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), sceneDetector=CalcEdge())
#     video.singleProcessPlay()

# def test1(fileName, scale):
#     #video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), filter=imgFilters.gaussianFiltering)
#     video = VideoPlayer(fileName, scale=scale, tracker=LucasKanade(), detector=FaceDetectorFilter(MyMTCNN()),sceneDetector=CalcHistogram())
#     video.singleProcessPlay(  )
#     # haar은 명암을 통해서 얼굴 인식하니까 명암비 조작이 더 좋을지도

def multiProcessPlayTest(fileName):
    #vl = Controller.startAndGetVideoLoader(fileName, processorNumber=8, bufSize=8, cfl=60,scale=2, tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), draw=True, transceiver=Transceiver(PickleSerializer(), GZipCompressor()))
    #vl = Controller.startAndGetVideoLoader(fileName, processorNumber=8, bufSize=8, cfl=60,scale=2, tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), draw=True)
    #vl = Controller.startAndGetVideoLoader(fileName, processorNumber=8, bufSize=8, cfl=60,scale=2, tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), draw=True, transceiver=Transceiver(PickleSerializer(), GZipCompressor()))
    vl = Controller.startAndGetVideoLoader(fileName, detectFrameCount=1, visionProcessorNumber=1, detectProcessorNumber=1, bufSize=16, cfl=60,scale=1, compressor=JpgCompressor, tracker=LucasKanade, detector=MyMTCNN,sceneDetector=CalcHistogram, draw=True)
    #vl = Controller.startAndGetVideoLoader(fileName, scale=2, tracker=LucasKanade(), filter = deblurFilters.wienerFiltering, detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), draw=True)
    #vl = Controller.startAndGetVideoLoader(fileName, scale=2, tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), draw=True)
    #vl = Controller.startAndGetVideoLoader(fileName, processorNumber=1, cfl=50)
    #vl = Controller.startAndGetVideoLoader(fileName, processorNumber=8, bufSize=16, cfl=60,scale=2, compressor=JpgCompressor(), tracker=LucasKanade(), detector=FaceDetectorFilter(HaarCascade()),sceneDetector=CalcHistogram(), draw=True, filter=deblurFilters.TotalVariationDeblurringFiltering)

    VideoPlayer(vl).play()
    print("종료")