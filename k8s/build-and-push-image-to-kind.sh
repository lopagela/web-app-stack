#!/bin/bash

IMAGE_FRONTEND=web-app-frontend
IMAGE_BACKEND=web-app-backend

echo "Enable docker buildkit"
export DOCKER_BUILDKIT=1

cd ../
echo "At the root=$(pwd) of the project, will create the 2 docker image required to run the web-app"

(
cd backend/
echo "Building backend here=$(pwd)"
docker build . -t $IMAGE_BACKEND
)

echo "Back here=$(pwd)"

(
cd frontend/
echo "Building frontend here=$(pwd)"
docker build . -t $IMAGE_FRONTEND
)

echo "Loading the docker images into the demo K8S cluster (kind)"
kind load docker-image $IMAGE_FRONTEND
kind load docker-image $IMAGE_BACKEND
