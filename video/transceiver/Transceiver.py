from video.transceiver import TransceiverInterface

class Transceiver(TransceiverInterface):

    def send(self, destination, value):
        destination.put(self._compressor.compress(self._serializer.serialization(value)))

    def receive(self, destination):
        if destination.empty():
            return False, None
        return True, self._serializer.deSerialization(self._compressor.decompress(destination.get()))