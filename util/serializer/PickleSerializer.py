import pickle

from util.serializer.SerializerInterface import SerializerInterface

class PickleSerializer(SerializerInterface):
    def serialization(self, value):
        return pickle.dumps(value)

    def deSerialization(self, value):
        return pickle.loads(value) 
    