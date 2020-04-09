#!/bin/bash

set -ex

cd ../../labbox_ephys_widgets

cd generated/labbox_ephys_widgets
pip install --no-deps -e .

cd ../../..
pip install --no-deps -e .