#!/bin/bash

set -e

docker pull mongo:latest
docker-compose rm -sf mongodb_dev || true
docker-compose up --build --abort-on-container-exit mongodb_dev
