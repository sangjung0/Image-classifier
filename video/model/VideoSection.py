from video.model.Frame import Frame
from util.compressor import CompressorInterface
class VideoSection:
    def __init__(self, index, frames = [], compressor:CompressorInterface = None):
        self.__index = index
        self.__frames = frames
        self.__compressor = compressor

    @property
    def index(self):
        return self.__index
    
    def append(self, frame:Frame):
        if self.__compressor is not None:
            imgs = frame.imgs
            keys = imgs.keys()
            for key in keys:
                imgs[key] = self.__compressor.compress(imgs[key])
        self.__frames.append(frame)

    def clear(self, index):
        self.__frames.clear()
        self.__index = index
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __len__(self):
        return len(self.__frames)
    
    def __iter__(self):
        return VideoSection.__VideoSectionIter(self.__frames, self.__compressor)
    
    class __VideoSectionIter:
        def __init__(self, frames, compressor:CompressorInterface):
            self.__index = 0
            self.__frames = frames
            self.__compressor = compressor
        
        def __next__(self):
            if self.__index < len(self.__frames):
                frame = self.__frames[self.__index]
                self.__index += 1
                if self.__compressor is not None:
                    imgs = frame.imgs
                    keys = imgs.keys()
                    for key in keys:
                        imgs[key] = self.__compressor.decompress(imgs[key])
                return frame
            raise StopIteration