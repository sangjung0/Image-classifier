from typing import Type

from video.logic.StopOverPointInterface import StopOverPointInterface

from video.model import Section
from video.scene_detector import Interface

class SceneDetector(StopOverPointInterface):
    def __init__(self, sceneDetector: Type[Interface]):
        self.__sceneDetector = sceneDetector

    def prepare(self) -> None:
        self.__sceneDetector = self.__sceneDetector()
        
    def processing(self, section:Section) -> Section:
        sceneDetector = self.__sceneDetector

        for frame in section:
            isNewScene = sceneDetector.isNewScene(frame.getFrame())
            if isNewScene : frame.isDetect = isNewScene
            frame.isNewScene = isNewScene

        return section
