#!/bin/bash

set -ex

docker build -t magland/labbox_ephys_base:latest .
docker push magland/labbox_ephys_base:latest