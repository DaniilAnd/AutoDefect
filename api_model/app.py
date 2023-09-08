import json
import shutil

import click
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from inference import RoadDefectModel
from utils import to_Image, sift_matching, to_dict, load_yaml

app = FastAPI()

DEVICE = "cpu"
BASE_MODELS = "best.pt"


@app.post("/update")
async def update_weight(file: UploadFile):
    """

    :param file:
    :return:
    """
    try:
        # TODO: Добавить чтобы веса автоматом подгружались из MLflow любые с тегом production
        global BASE_MODELS
        file_path = f"./{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
            BASE_MODELS = file_path

        return JSONResponse(content={"message": "Файл успешно загружен"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@app.post("/detection")
async def detection(file: UploadFile = File(...), detection_threshold: float = 0.2) -> object:
    """
    Detection road defect
    :rtype: object json response
    :param file: binary image for inference model
    :param detection_threshold: confidence model
    :return: 
    """
    # TODO: Add pydantic
    global DEVICE, BASE_MODELS
    file = file.file.read()
    image = to_Image(file)
    model = RoadDefectModel(BASE_MODELS)
    result = model.get_predict(image, detection_threshold)
    bbox = np.array(result.xyxy)
    dict_schema = to_dict(bbox)
    print(dict_schema)
    return dict_schema


@app.post("/compare")
async def compare_img(file_first: UploadFile = File(...), file_second: UploadFile = File(...)) -> dict:
    """
    Compare images for antispam in-app
    :rtype: object
    :param file_first: binary image for inference model
    :param file_second: binary image for inference model
    :return:
    """
    result = sift_matching(file_first, file_second)
    return {"result": result}


@click.command()
@click.option('--app_conf_path', 'app_conf_path')
@click.option('--port', 'port', type=int)
@click.option('--host', 'host', type=str, default='0.0.0.0', required=False)
def start_app(app_conf_path: str = "config.yaml", port: int = 3000, host: str = '0.0.0.0') -> None:
    """
    Script to start inference service.

    Parameters
    ----------
    app_conf_path: str
        path to app config
    port: int
        port
    host: str
        host
    """
    global DEVICE, BASE_MODELS
    DEVICE = load_yaml(app_conf_path)['device']
    BASE_MODELS = load_yaml(app_conf_path)['base_models']
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_app()
