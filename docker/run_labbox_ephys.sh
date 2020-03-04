#!/bin/bash

set -e

export JUPYTERLAB_TOKEN=secret-token
export LABBOX_EPHYS_KILL_CODE=killcode

if [[ -z "$KACHERY_STORAGE_DIR" ]]; then
    echo "Environment variable not set: KACHERY_STORAGE_DIR" 1>&2
    exit 1
fi

if [[ -z "$LABBOX_EPHYS_PORT" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_PORT" 1>&2
    exit 1
fi

if [[ -z "$LABBOX_EPHYS_JUPYTERLAB_PORT" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_JUPYTERLAB_PORT" 1>&2
    exit 1
fi

if [[ -z "$LABBOX_EPHYS_DATA_DIR" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_DATA_DIR" 1>&2
    exit 1
fi

if [[ -z "$LABBOX_EPHYS_MONGO_DATA_DIR" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_MONGO_DATA_DIR" 1>&2
    exit 1
fi

if [[ -z "$LABBOX_EPHYS_HOME" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_HOME" 1>&2
    exit 1
fi

if [[ -z "$LABBOX_EPHYS_SOURCE_DIR" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_SOURCE_DIR" 1>&2
    exit 1
fi

export USER_ID=`id -u`
export GROUP_ID=`id -g`

cd ..
docker build -t labbox_ephys:latest -f docker2/Dockerfile .
cd docker2

docker pull mongo:latest
docker-compose rm -sf mongodb || true
docker-compose rm -sf jupyterlab || true
docker-compose rm -sf gui || true
docker-compose up --build --abort-on-container-exit

# docker-compose up --abort-on-container-exit jupyterlab
