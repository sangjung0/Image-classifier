from process.model.Image import Image

from process.compressor import CompressorInterface

class Section:
    def __init__(self, index:int, imgs:list = [], compressor:CompressorInterface = None):
        self.__index = index
        self.__imgs = imgs
        self.__compressor = compressor

    @property
    def index(self) -> int:
        return self.__index

    @property
    def imgs(self) -> list[Image]:
        return self.__imgs
    
    def append(self, img:Image) -> None:
        self.__imgs.append(img)

    def compress(self) -> None:
        self.__cps(self.__compressor.compress, "This frame is already compressed", True)

    def deCompress(self) -> None:
        self.__cps(self.__compressor.decompress, "This frame is already deCompressed", False)

    def __cps(self, logic:callable, msg:str, isCompress:bool) -> None:
        if self.__compressor is not None:
            for f in self.__imgs:
                data = f.data
                for key in data:
                    if isinstance(data[key], bytes) == isCompress:
                        raise Exception(msg)
                    data[key] = logic(data[key])
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __len__(self):
        return len(self.__imgs)
    
    def __iter__(self):
        return iter(self.__imgs)
