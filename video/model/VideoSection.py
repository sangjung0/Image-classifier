class VideoSection:
    def __init__(self, index, frames = [], compressor = None):
        self.__index = index
        self.__frames = frames
        self.__compressor = compressor

    @property
    def index(self):
        return self.__index

    @property
    def frames(self):
        return self.__frames
    
    def append(self, frame):
        self.__frames.append(frame if self.__compressor is None else self.__compressor(frame))

    def clear(self, index):
        self.__frames.clear()
        self.__index = index
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __len__(self):
        return len(self.__frames)