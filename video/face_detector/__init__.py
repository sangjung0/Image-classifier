"""
얼굴 탐지 알고리즘
"""

from video.face_detector.DetectorInterface import DetectorInterface

from video.face_detector.HaarCascade import HaarCascade
from video.face_detector.MyMTCNN import MyMTCNN

__all__ = ['MyMTCNN', 'HaarCascade', 'DetectorInterface']
__version__ = '0.1'