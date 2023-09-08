FROM python:alpine3.18

WORKDIR /server
COPY . .

EXPOSE $SERVER_PORT

RUN python -m pip install -r requirements.txt


CMD ['uvicorn', 'src.main:app', '--reload']
