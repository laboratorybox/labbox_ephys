#!/bin/bash

set -ex

cd ../../labbox_ephys_widgets
reactopya install || true

# Somehow we need the following line because pip install -e . has a segfault. Don't know why.
cd generated/labbox_ephys_widgets
pip install --no-deps -e .

cd ../../../reactopya/reactopya/reactopya_server && yarn install && yarn build