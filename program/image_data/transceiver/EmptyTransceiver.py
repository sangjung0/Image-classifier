from process.transceiver import TransceiverInterface

class EmptyTransceiver(TransceiverInterface):

    def send(self, destination, value):
        destination.put(value)

    def receive(self, destination):
        if destination.empty():
            return False, None
        return True, destination.get()