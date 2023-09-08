from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api_model.model import Images
from sensitive_data import *

if __name__ == "__main__":

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, data in enumerate(list_coor):
        new_image = Images(id_user=i, name_images=f'image{i}.jpg',
                           bbox_json={'x': 10, 'y': 20, 'width': 100, 'height': 200},
                           gps_coordinates={"x": data[0], "y": data[1]})
        session.add(new_image)
        session.commit()
