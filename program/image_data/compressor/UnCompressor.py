from image_data.compressor.Interface import Interface

class UnCompressor(Interface):

    def compress(self, value: bytes) -> bytes: 
        return value

    def decompress(self, value: bytes) -> bytes:
        return value