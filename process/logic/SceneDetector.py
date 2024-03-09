from typing import Type

from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section
from process.scene_detector import Interface

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
