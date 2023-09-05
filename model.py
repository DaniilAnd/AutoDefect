from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import datetime

from api_model.sensitive_data import connection_string

Base = declarative_base()


class Images(Base):
    __tablename__ = 'Images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer)
    name_images = Column(String)
    bbox_json = Column(JSON)
    time_escalation = Column(DateTime, default=datetime.datetime.utcnow)
    gps_coordinates = Column(JSON)


if __name__ == "__main__":
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)

