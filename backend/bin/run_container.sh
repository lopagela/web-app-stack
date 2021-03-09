#!/bin/bash

IMAGE_NAME="web-app-stack-backend"

docker build . -t ${IMAGE_NAME} && \
docker run -p 8000:8000 -it --rm ${IMAGE_NAME}