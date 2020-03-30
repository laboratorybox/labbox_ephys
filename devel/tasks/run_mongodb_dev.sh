#!/bin/bash

set -e

docker pull mongo:4.2.5
docker stop mongodb_dev || true
docker rm mongodb_dev || true
docker-compose up --build --abort-on-container-exit mongodb_dev
