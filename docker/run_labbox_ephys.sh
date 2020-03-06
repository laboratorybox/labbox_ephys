#!/bin/bash

set -ex

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
docker build -t labbox_ephys:latest -f docker/Dockerfile .
cd docker

# Now change the uid of the user within the container
# updateUID.Dockerfile was copied from the ms-vscode-remote.remote-containers-0.101.1 extension
# I suppose we should rewrite it to comply with license
docker build \
    -f $PWD/updateUID/updateUID.Dockerfile \
    -t labbox_ephys_updateuid:latest \
    --build-arg BASE_IMAGE=labbox_ephys:latest \
    --build-arg REMOTE_USER=labbox \
    --build-arg NEW_UID=${USER_ID} \
    --build-arg NEW_GID=${GROUP_ID} \
    --build-arg IMAGE_USER=root \
    $PWD/updateUID

docker stop labbox_ephys_compute_resource || true
docker rm labbox_ephys_compute_resource || true

docker pull mongo:latest
docker-compose rm -sf mongodb || true
docker-compose rm -sf jupyterlab || true
docker-compose rm -sf gui || true
docker-compose rm -sf compute_resource || true
docker-compose up --build --abort-on-container-exit

docker stop labbox_ephys_compute_resource || true
docker rm labbox_ephys_compute_resource || true

# docker-compose up --abort-on-container-exit jupyterlab
