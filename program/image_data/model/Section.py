class Section: #섹션에 인덱스 필요없으면 버리자
    def __init__(self, index:int):
        self.__index = index
        self.__data = []
        self.__dataIndex = []

    @property
    def index(self) -> int:
        return self.__index

    @property
    def data(self) -> list[object]:
        return self.__data
    
    @property
    def dataIndex(self) -> list[int]:
        return self.__dataIndex
    
    def append(self, data:object, dataIndex) -> None:
        self.__data.append(data)
        self.__dataIndex.append(dataIndex)
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __len__(self):
        return len(self.__data)
    
    def __iter__(self):
        return iter(self.__data)
