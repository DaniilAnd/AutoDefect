FROM nvidia/cuda:11.6.2-devel-ubuntu20.04 as base
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Moscow
#    HTTP_PROXY="http://10.100.205.204:3128" \
#    HTTPS_PROXY="http://10.100.205.204:3128" \
#    http_proxy="http://10.100.205.204:3128" \
#    https_proxy="http://10.100.205.204:3128" \
#    no_proxy="localhost,localdomain,127.0.0.1,etc" \
#    NO_PROXY="localhost,localdomain,127.0.0.1,etc"

ARG PORT_ID=3000
ARG HOST=0.0.0.0
ENV PORT_ID ${PORT_ID}
ENV HOST ${HOST}



RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.9 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN   apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python3.9 -m pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116
COPY ./api_model ./api_model
COPY ./requirements.txt .
RUN python3.9 -m pip install -r requirements.txt
#RUN python3.9 -m pip install -e .

WORKDIR ./api_models

EXPOSE ${PORT_ID}
CMD cd api_models  && python3.9 -m uvicorn app:app --host ${HOST} --workers 3 --port ${PORT_ID}
