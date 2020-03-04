#!/bin/bash

while true; do
  git pull
  ./run_labbox_ephys.sh
  sleep 5
done
