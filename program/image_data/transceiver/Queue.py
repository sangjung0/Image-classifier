from multiprocessing import Queue as Q

from image_data.transceiver import Interface

class Queue(Interface):

    def send(self, destination: Q, value: object) -> None:
        destination.put(self._compressor.compress(self._serializer.serialization(value)))

    def receive(self, destination: Q) -> object:
        if destination.empty():
            return False, None
        return True, self._serializer.deSerialization(self._compressor.decompress(destination.get()))