#!/bin/bash

# TODO improve with https://stackoverflow.com/a/246128
SCRIPT_SOURCE="bin/local-development"
VENV=.venv

if [[ ! -d "${SCRIPT_SOURCE}/${VENV}" ]]; then
  echo "Creating a python3.9 venv at='${SCRIPT_SOURCE}/${VENV}'" >&2
  python3.9 -m venv "$VENV"
  source "${VENV}/bin/activate"
  pip install --upgrade pip
  pip install docker-compose
  deactivate
fi

source "${VENV}/bin/activate"

docker-compose -f "${SCRIPT_SOURCE}/docker-compose.yml" up \
               --abort-on-container-exit \
               --build \
               --remove-orphans
