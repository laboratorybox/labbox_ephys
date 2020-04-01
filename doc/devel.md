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

export REACTOPYA_SOURCE_DIR=/the/path/to/src/reactopya
export HITHER2_SOURCE_DIR=/the/path/to/src/hither2
export KACHERY_SOURCE_DIR=/the/path/to/src/kachery
export SPIKEFOREST2_SOURCE_DIR=/the/path/to/src/spikeforest2
export LABBOX_EPHYS_SOURCE_DIR=/the/path/to/src/labbox_ephys

export LABBOX_EPHYS_PORT=5001
export LABBOX_EPHYS_JUPYTERLAB_PORT=8891
export LABBOX_EPHYS_DATA_DIR=/some/path/to/labbox_ephys_data
export LABBOX_EPHYS_HOME=/some/path/to/labbox_ephys_home

export LABBOX_EPHYS_MONGO_URI="fill-in-the-mongo-uri"
export LABBOX_EPHYS_KACHERY_READWRITE_PASSWORD="fill-in-the-password"
```

**Important:** After modifying these variables, log out and log back in again to make sure that they take effect.

## Installation

Switch to the labbox_ephys source directory (cloned above) and open in vscode

```
cd labbox_ephys
code .
```

Install the following vscode extension: ms-vscode-remote.remote-containers

There will be a green button in the lower-left part of the vscode window. Click on that and select the "reopen in container".

This will begin building a docker image and open the development environment inside the container. See the .devcontainer directory for information about exactly what is being installed.

**Important:** If environment variables or the content of the .devcontainer have changed, you will also need to rebuild the container.

## Do a one-time installation of the reactopya server

Within the container

```
cd /workspaces/reactopya/reactopya/reactopya_server
yarn install
yarn build
```

## Start the services within the container

Use `Ctrl+Shift+P` to open the vscode command window and then run the `Run Task` command. You will see a list of development tasks.

Each time you open the reopen the development environment in the vscode container, you will need to rebuild the application by running the `build-gui-dev` task.

To start the system application in development mode, run the the following services:
* `gui-dev`
* `compute-resource-dev`
* `jupyterlab-dev`

## Open a browser

Point google chrome to `http://localhost:5001/app/labbox_ephys

## To develop individual widgets

First run the task: gui-install-dev

Then run the task: gui-start-dev

Then open a web browser to http://localhost:5050

Open labbox_ephys_widgets/dev_widget.json
