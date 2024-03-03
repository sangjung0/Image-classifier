import pickle

from project_constants import PROCESSOR_STOP
from video import Loader
from util.util import Loger

class SaveFace:
    def __init__(self, videoLoader:Loader):
        self.__videoLoader = videoLoader

    def save(self):
        self.__videoLoader.run()
        it = iter(self.__videoLoader)
        loger = Loger("SaveImg")
        loger("start")
        idx = 0
        all_face = []
        while True:
            try:
                flag, ret, frame = next(it)
                if ret:
                    if idx % 100 == 0:
                        loger(f"{idx} 완료")
                    for f in frame.face:
                        f.points.clear()
                        all_face.append(f)
                    idx+=1
                elif flag == PROCESSOR_STOP:
                    break
            except Exception as err:
                print(err)
                break
        self.__videoLoader.stop()
        with open('faces.pkl', 'wb') as f:
            pickle.dump(all_face, f)
        return

class LoadFace:
    def __init__(self, fileName:str):
        with open(fileName, 'rb') as f:
            self.__faces = pickle.load(f)

    def load(self):
        return self.__faces