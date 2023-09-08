from abc import ABC, abstractmethod
from os import path

from ultralytics import YOLO


class BaseModel(ABC):
    @abstractmethod
    def get_predict(self, img, conf, device):
        """

        :param device:
        :param img:
        :param conf:
        """
        pass


class RoadDefectModel(BaseModel):
    def __init__(self, model_path: str):
        """

        :param model_path:
        """
        self.model_path = path.abspath(model_path)
        self.model = YOLO(model_path)

    def get_predict(self, img, confidence, device):
        """

        :param device:
        :param img:
        :param confidence:
        :return:
        """
        results = self.model(img, conf=confidence, device=device)
        results = results[0].boxes

        return results
