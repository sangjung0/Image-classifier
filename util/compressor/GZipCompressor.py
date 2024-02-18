import gzip
import io

from util.compressor.CompressorInterface import CompressorInterface

class GZipCompressor(CompressorInterface):

    def compress(self, value):
        with gzip.GzipFile(fileobj=io.BytesIO(), mode='wb') as f:
            f.write(value)
            return f.getvalue()
        
    def decompress(self, value):
        with gzip.GzipFile(fileobj=io.BytesIO(value), mode='rb') as f:
            return f.read()
