from core.scheduler.dto import PacketData

class Packet:
    """멀티 프로세싱에 데이터 전달에 사용 할 패킷"""
    def __init__(self, datas:list[PacketData] = []) -> None:
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

