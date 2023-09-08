# AutoDefect
<h2>Стек технологий<h2/>
YOLOv8, FastApi, Kornia, OpenCV. Обучение MLflow + Optuna <br/>
Позднее будут добавлены линтеры, типизация
<h2>Сборка Dockerfile локально<h2/>
docker build -t images_autodefect_api_models -f ..\Dockerfile_api_models . <br />
docker run  -d --name container_autodefect_api_models -p 3000:3000 images_autodefect_api_models <br />

<h2>Сборка через Harbor (ci/cd gitlab) <h2/>
- build stage <br/>
docker login -u ${REGISTRY_LOGIN} -p ${REGISTRY_PASSWORD} ${REGISTRY_URL} <br/>
docker build -t ${DOCKER_IMAGE_NAME}:${SERVICE_VERSION} -f ..\Dockerfile_api_models . --build-arg PORT_ID=${APP_PORT} <br/>
docker tag ${DOCKER_IMAGE_NAME} ${REGISTRY_URL}/library/${DOCKER_IMAGE_NAME}:${SERVICE_VERSION}
echo $DOCKER_AUTH > ~/.docker/config.json
docker push ${REGISTRY_URL}/library/${DOCKER_IMAGE_NAME}:${SERVICE_VERSION}
- deploy stage <br/>
docker login -u ${REGISTRY_LOGIN} -p ${REGISTRY_PASSWORD} ${REGISTRY_URL} <br/>
docker pull ${REGISTRY_URL}/library/${DOCKER_IMAGE_NAME}:${SERVICE_VERSION} <br/>
docker run  -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE_NAME}:${SERVICE_VERSION} <br/>









<hr>
<img src="logo.jpg">