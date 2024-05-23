from program.core.scheduler.processor.Processor import Processor


class FaceDetector(Processor):
    def __init__(self, buf_size: int):
        super().__init__(buf_size)