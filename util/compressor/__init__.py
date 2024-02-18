"""
압축 패키지
"""


from util.compressor.CompressorInterface import CompressorInterface
from util.compressor.GZipCompressor import GZipCompressor
from util.compressor.UnCompressor import UnCompressor
from util.compressor.JpgCompressor import JpgCompressor

__all__ = ['CompressorInterface', 'GZipCompressor', 'UnCompressor', 'JpgCompressor']
__version__ = '0.1'