class VideoSection:
    def __init__(self, index:int, frames):
        self.__index = index
        self.__frames = frames

    @property
    def index(self):
        return self.__index

    @property
    def frames(self):
        return self.__frames
    
    def __lt__(self, other):
        return self.index < other.index