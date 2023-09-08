from abc import ABC, abstractmethod
from os import path

from ultralytics import YOLO


class BaseModel(ABC):
    @abstractmethod
    def get_predict(self, img, conf):
        """

        :param img:
        :param conf:
        """
        pass


class RoadDefectModel(BaseModel):
    def __init__(self, model_path: str = path.abspath("best.pt")):
        """

        :param model_path:
        """
        self.model = YOLO(model_path)

    def get_predict(self, img, confidence):
        """

        :param img:
        :param confidence:
        :return:
        """
        results = self.model(img, conf=confidence, boxes=True, save=True)
        results = results[0].boxes

        return results
