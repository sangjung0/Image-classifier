from process import *
from process.compressor import JpgCompressor
from process.face_detector import MyMTCNN
from view import Main

def imageTest(path:str) -> None:
    loader = Controller.startAndGetVideoLoader(path, scale=2, cfl=20, bufSize=5, compressor=JpgCompressor, detector=MyMTCNN, draw=True)
    VideoPlayer(loader).play()

def guiTest(path:str) -> None:
    app, window = Main.start(path)
    app.exec_()