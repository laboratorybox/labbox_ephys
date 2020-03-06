#!/bin/bash

set -e

docker pull mongo:latest
docker stop mongodb_dev || true
docker rm mongodb_dev || true
docker-compose up --build --abort-on-container-exit mongodb_dev
