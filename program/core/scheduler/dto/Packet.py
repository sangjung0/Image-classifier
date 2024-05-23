from program.core.scheduler.dto.PacketData import PacketData


class Packet:
    def __init__(self):
        self.__data: list[PacketData]

    def get_data(self) -> list[PacketData]: pass

    def append(self, data: PacketData): pass

    def compress(self): pass

    def decompress(self): pass

    def __iter__(self) -> iter: pass

    def __len__(self) -> int: pass

