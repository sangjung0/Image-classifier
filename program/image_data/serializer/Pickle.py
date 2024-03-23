import pickle

from image_data.serializer.Interface import Interface

class Pickle(Interface):
    def serialization(self, value):
        return pickle.dumps(value)

    def deSerialization(self, value):
        return pickle.loads(value) 
    