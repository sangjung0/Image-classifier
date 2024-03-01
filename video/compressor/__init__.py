"""
압축 패키지
"""


from video.compressor.CompressorInterface import CompressorInterface
from video.compressor.GZipCompressor import GZipCompressor
from video.compressor.UnCompressor import UnCompressor
from video.compressor.JpgCompressor import JpgCompressor

__all__ = ['CompressorInterface', 'GZipCompressor', 'UnCompressor', 'JpgCompressor']
__version__ = '0.1'