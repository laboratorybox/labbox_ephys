#!/bin/bash
set -ex

cd tests
exec python -m pytest --cov labbox_ephys --cov-report=term --cov-report=xml:../cov.xml -s -rA --durations=0 "$@"