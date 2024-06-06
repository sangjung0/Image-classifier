from core.scheduler.dto import PacketData

class Packet:
    def __init__(self, datas:list[PacketData] = []):
        self.__data: list[PacketData] = datas
        
    @property
    def data(self) -> list[PacketData]:
        return self.__data

    def append(self, data: PacketData) -> None:
        self.__data.append(data)

    def __iter__(self) -> iter:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

