from datetime import datetime
from pydantic import BaseModel


class Report(BaseModel):
    user_id: int
    image_path: str
    bbox_json: dict
    time_escalation: datetime
    gps_coordinates: dict
