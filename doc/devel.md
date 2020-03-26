## Openning labbox_ephys in a development environment

## Prerequisites

Recommended operating system: Linux

Install the following
* vscode
* docker

## Clone some repositories

```
cd /some/path/to/src
git clone https://github.com/laboratorybox/labbox_ephys
git clone https://github.com/laboratorybox/hither2
git clone https://github.com/flatironinstitute/kachery
git clone https://github.com/flatironinstitute/reactopya
git clone https://github.com/flatironinstitute/spikeforest2
```

## Set some environment variables

Add the following lines to ~/.bashrc file (substituting as needed)

```
export KACHERY_STORAGE_DIR=/some_path/to/large/temporary/files

export REACTOPYA_SOURCE_DIR=/some/path/to/src/reactopya
export HITHER2_SOURCE_DIR=/some/path/to/src/hither2
export KACHERY_SOURCE_DIR=/some/path/to/src/kachery
export SPIKEFOREST2_SOURCE_DIR=/some/path/to/src/spikeforest2
export LABBOX_EPHYS_SOURCE_DIR=/some/path/to/src/labbox_ephys

export LABBOX_EPHYS_PORT=5001
export LABBOX_EPHYS_JUPYTERLAB_PORT=8891
export LABBOX_EPHYS_DATA_DIR=/some/path/to/labbox_ephys_data
export LABBOX_EPHYS_MONGO_DATA_DIR=/some/path/to/labbox_ephys_mongo_data
export LABBOX_EPHYS_HOME=/some/path/to/labbox_ephys_home
```

Then to make sure these take effect, log out and log back in again

## Installation

First, clone the repository:

```
git clone https://github.com/laboratorybox/labbox_ephys
cd labbox_ephys
```

Then open in vscode

```
code .
```

Install the following vscode extension: ms-vscode-remote.remote-containers

There will be a green button in the lower-left part of the vscode window. Click on that and select the "reopen in container".

This will begin building a docker image and open the development environment inside the container. See the .devcontainer directory for information about exactly what is being installed.

## Do a one-time installation of the reactopya server

Within the container

```
cd /workspaces/reactopya/reactopya/reactopya_server
yarn install
yarn build
```

## 

## Start the services within the container

USe `Ctrl+Shift+P` to open the vscode command window and then run the `Run Task` command. Select to run the `all-services` task.

## Open a browser

## To develop individual services

First run the task: gui-install-dev

Start the mongo database by running the task: mongodb-dev

Then run the task: gui-start-dev

Then open a web brower to http://localhost:5050

Open labbox_ephys_widgets/dev_widget.json
