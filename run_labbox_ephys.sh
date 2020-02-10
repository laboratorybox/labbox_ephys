#!/bin/bash

# You must set the following environment variables
#     LABBOX_EPHYS_PORT
#     KACHERY_STORAGE_DIR
#     EPHYS_DATA_DIR

if [[ -z "$LABBOX_EPHYS_PORT" ]]; then
    echo "Environment variable not set: LABBOX_EPHYS_PORT" 1>&2
    exit 1
fi

if [[ -z "$KACHERY_STORAGE_DIR" ]]; then
    echo "Environment variable not set: KACHERY_STORAGE_DIR" 1>&2
    exit 1
fi

if [[ -z "$EPHYS_DATA_DIR" ]]; then
    echo "Environment variable not set: EPHYS_DATA_DIR" 1>&2
    exit 1
fi

export USER_ID=`id -u`
export GROUP_ID=`id -g`
docker-compose up --build