import gzip
import io

from image_data.compressor.Interface import Interface

class GZip(Interface):

    def compress(self, value):
        with io.BytesIO() as buf:
            with gzip.GzipFile(fileobj=buf, mode='wb') as f:
                f.write(value)
            return buf.getvalue()
        
    def decompress(self, value):
        with gzip.GzipFile(fileobj=io.BytesIO(value), mode='rb') as f:
            return f.read()
