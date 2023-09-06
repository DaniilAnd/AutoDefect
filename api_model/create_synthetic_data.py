import json

import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_model.inference import RoadDefectModel
from model import Images
from sensitive_data import list_coor, connection_string
import os

from api_model.utils import load_Image, to_dict

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
        bbox = np.array(result.xyxy)
        dict_schema = to_dict(bbox)
        json_schema = json.dumps(dict_schema)
        print(dict_schema)
        new_image = Images(id_user=1, name_images=f'{path_img}',
                           bbox_json=json_schema,
                           gps_coordinates={"x": coor[0], "y": coor[1]})
        session.add(new_image)
        session.commit()
