from util import VideoData
from face_detector import MyMTCNN, HaarCascade

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