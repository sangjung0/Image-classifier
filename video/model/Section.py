from video.model.Frame import Frame
from util.compressor import CompressorInterface

class Section:
    def __init__(self, index:int, frames:list = [], compressor:CompressorInterface = None):
        self.__index = index
        self.__frames = frames
        self.__compressor = compressor

    @property
    def index(self):
        return self.__index

    @property
    def frames(self):
        return self.__frames

    def next(self):
        self.__index = self.__index + 1
        self.__frames.clear()
    
    def append(self, frame:Frame):
        self.__frames.append(frame)

    def compress(self):
        if self.__compressor is not None:
            for f in self.__frames:
                imgs = f.imgs
                for key in imgs:
                    if isinstance(imgs[key], bytes):
                        raise Exception("This frame is already compressed")
                    imgs[key] = self.__compressor.compress(imgs[key])

    def deCompress(self):
        if self.__compressor is not None:
            for f in self.__frames:
                imgs = f.imgs
                for key in imgs:
                    if not isinstance(imgs[key], bytes):
                        raise Exception("This frame is already deCompressed")
                    imgs[key] = self.__compressor.decompress(imgs[key])
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __len__(self):
        return len(self.__frames)
    
    def __iter__(self):
        return iter(self.__frames)
