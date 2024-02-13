class VideoSection:
    def __init__(self, index:int, frameAry):
        self.__index = index
        self.__frameAry = frameAry

    @property
    def index(self):
        return self.__index

    @property
    def frameAry(self):
        return self.__frameAry