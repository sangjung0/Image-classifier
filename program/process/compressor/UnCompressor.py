from process.compressor.CompressorInterface import CompressorInterface

class UnCompressor(CompressorInterface):

    def compress(self, value: bytes) -> bytes: 
        return value

    def decompress(self, value: bytes) -> bytes:
        return value