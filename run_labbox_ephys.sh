#!/bin/bash

set -e

# You must set the following environment variables
#     LABBOX_EPHYS_PORT
#     KACHERY_STORAGE_DIR
#     LOCAL_DATA_DIR
#     MONGO_DATA_DIR

source ./config.default.sh
source ./config.user.sh

if [[ -z "$LABBOX_EPHYS_PORT" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_PORT" 1>&2
    exit 1
fi

if [[ -z "$KACHERY_STORAGE_DIR" ]]; then
    echo "Environment variable not set: KACHERY_STORAGE_DIR" 1>&2
    exit 1
fi

if [[ -z "$LOCAL_DATA_DIR" ]]; then
    echo "Environment variable not set: LOCAL_DATA_DIR" 1>&2
    exit 1
fi

if [[ -z "$MONGO_DATA_DIR" ]]; then
    echo "Environment variable not set: MONGO_DATA_DIR" 1>&2
    exit 1
fi

export USER_ID=`id -u`
export GROUP_ID=`id -g`

docker build -t labbox_ephys_gui:latest gui
docker pull mongo:latest
docker-compose up --build