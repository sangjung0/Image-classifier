"""
직렬화 패키지
"""


from video.serializer.PickleSerializer import PickleSerializer
from video.serializer.SerializerInterface import SerializerInterface

__all__ = ['PickleSerializer', 'SerializerInterface']
__version__ = '0.1'