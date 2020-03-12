#!/bin/bash

set -ex

sudo usermod -aG docker vscode
newgrp docker

# reactopya
cd /workspaces/reactopya
pip install --no-deps -e .
echo "export PATH=/workspaces/reactopya/bin:\$PATH" >> ~/.bashrc

# hither2
cd /workspaces/hither2
pip install --no-deps -e .
echo "export PATH=/workspaces/hither2/bin:\$PATH" >> ~/.bashrc

# kachery
cd /workspaces/kachery
pip install --no-deps -e .

# spikeforest2
cd /workspaces/spikeforest2
pip install --no-deps -e .

# labbox_ephys
cd /workspaces/labbox_ephys
pip install --no-deps -e .

cat <<EOT >> ~/.bashrc
alias gs="git status"
alias gpl="git pull"
alias gps="git push"
alias gpst="git push && git push --tags"
alias gc="git commit"
alias ga="git add -u"
EOT

