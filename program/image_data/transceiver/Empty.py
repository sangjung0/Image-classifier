from image_data.transceiver import Interface

class Empty(Interface):

    def send(self, destination, value):
        destination.put(value)

    def receive(self, destination):
        if destination.empty():
            return False, None
        return True, destination.get()