from image_data import *
from image_data.face_detector import MyMTCNN
from view import Main

def imageTest(path:str) -> None:
    loader = Controller.startAndGetVideoLoader(
        path, MyMTCNN
    )
    loader.run()
    for flag, ret, data in loader:
        if ret:
            print(data)

def guiTest(path:str) -> None:
    app, window = Main.start(path)
    app.exec_()