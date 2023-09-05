import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_model.inference import RoadDefectModel
from api_model.model import Images
from data.sensitive_data import list_coor, connection_string
import os

from api_model.utils import load_Image

if __name__ == "__main__":

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    path = "data"
    path_imgs = os.listdir(path)
    for coor, img_name in zip(list_coor, path_imgs):
        path_img = os.path.join(path, img_name)
        img = load_Image(path_img)
        model = RoadDefectModel()
        result = model.get_predict(img, 0.1)
        print(np.array(result.xyxy))
        # new_image = Images(id_user=i, name_images=f'image{i}.jpg',
        #                    bbox_json={'x': 10, 'y': 20, 'width': 100, 'height': 200},
        #                    gps_coordinates={"x": data[0], "y": data[1]})
        # session.add(new_image)
        # session.commit()
