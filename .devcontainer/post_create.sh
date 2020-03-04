#!/bin/bash

sudo usermod -aG docker vscode
newgrp docker

cd /workspaces/hither2
pip install -e .

cd /workspaces/kachery
pip install -e .