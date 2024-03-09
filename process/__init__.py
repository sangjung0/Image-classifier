"""
비디오 재생 패키지
"""

from process.VideoPlayer import VideoPlayer
from process.Loader import Loader
from process.Controller import Controller

__all__ = ['VideoPlayer', 'Controller', 'Loader', "face_detector", "tracker"]
__version__='0.1'