import json

import numpy as np
from fastapi import FastAPI, UploadFile, File

from inference import RoadDefectModel
from utils import to_Image, sift_matching, to_dict

app = FastAPI()

"""
TODO: 05.09
0. Общий задачник ?
1. Выбор проекта и что хотим показать на конечном питче.
2. Задачи на неделю и определение в какое время подводим результаты дня.
3. Инициализация БД, дообучение модели,
4. Сопряжение частей проекта в одно пространство || репу,
5. Анализ взаимодействия с госорганами системы и посмотреть какой уровень госоргана связанная с дорожным покрытием 
   (районный, областной, региональный, федеральный),
6. Рыба презы
7. Деплой системы куда ?
8. Определение кол-во источников данных (модуль из машины, отправка заявки на сайте, отправка через бота ТГ - пример)


CREATE TABLE Images (
    id SERIAL PRIMARY KEY,
    id_user INT,
    name_images VARCHAR(255),
    bbox_json JSONB,
    gps_coordinates JSONB
    time_escalation TIMESTAMP
);


TODO: 06.09
0. Итог предыдущего дня aka доделка долга
1. Определение форматов взаимодействия между модулями системы (какие пары ключ-значения в json как пример, ip)
2. Подготовка тестовых данных
3. Эконом эффект || расчёт сервера
4. Анализ похожих систем

"""


@app.post("/detection")
async def detection(file: UploadFile = File(...), detection_threshold: float = 0.2) -> object:
    """
    Detection road defect
    :rtype: object json response
    :param file: binary image for inference model
    :param detection_threshold: confidence model
    :return: 
    """
    # TODO: Добавить возвращение json с классами и боксами
    file = file.file.read()
    image = to_Image(file)
    model = RoadDefectModel()
    result = model.get_predict(image, detection_threshold)
    bbox = np.array(result.xyxy)
    dict_schema = to_dict(bbox)
    print(dict_schema)
    return dict_schema


@app.post("/compare")
async def compare_img(file_first: UploadFile = File(...), file_second: UploadFile = File(...)):
    """
    Compare images for antispam in-app
    :rtype: object
    :param file_first: binary image for inference model
    :param file_second: binary image for inference model
    :return:
    """
    # TODO: Дописать функцию сравнения двух изображений
    sift_matching(file_first, file_second)
    return " "
