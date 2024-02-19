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
        self.compress(frame)
        self.__frames.append(frame)

    def compress(self, frame:Frame):
        if self.__compressor is not None:
            imgs = frame.imgs
            keys = imgs.keys()
            for key in keys:
                if isinstance(imgs[key], bytes):
                    raise Exception("This frame is already compressed")
                imgs[key] = self.__compressor.compress(imgs[key])

    def deCompress(self, frame:Frame):
        if self.__compressor is not None:
            imgs = frame.imgs
            keys = imgs.keys()
            for key in keys:
                if not isinstance(imgs[key], bytes):
                    raise Exception("This frame is already deCompressed")
                imgs[key] = self.__compressor.decompress(imgs[key])
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __len__(self):
        return len(self.__frames)
    
    def __iter__(self):
        return Section.__SectionIter(self.__frames, self.deCompress)
    
    class __SectionIter:
        def __init__(self, frames:list, deCompressor:CompressorInterface):
            self.__framesIter = iter(frames)
            self.__deCompressor = deCompressor
        
        def __next__(self):
            frame = next(self.__framesIter)
            self.__deCompressor(frame)
            return frame
