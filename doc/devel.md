## Openning labbox_ephys in a development environment

## Prerequisites

Pperating system: Linux or Mac

Install the following
* vscode
    - Ensure that `code` is available on command-line
    - [On Mac](https://code.visualstudio.com/docs/setup/mac)
    - On Linux there are various guides
* docker
    - Ensure that `docker` is available on command-line
    - [On Mac](https://docs.docker.com/docker-for-mac/install/)
    - [On Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)

## Clone some repositories

First you should create a directory on your machine where source code will be stored. Let's call it `/some/path/to/src`.

```
cd /some/path/to/src
git clone https://github.com/laboratorybox/labbox_ephys
git clone https://github.com/laboratorybox/hither2
git clone https://github.com/flatironinstitute/kachery
git clone https://github.com/flatironinstitute/reactopya
git clone https://github.com/flatironinstitute/spikeforest2
```

## Set some environment variables

Add the following lines to ~/.bashrc or ~/.bash_profile file (substituting as needed).

**Important:** After modifying these variables, log out and log back in again to make sure that they take effect.


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

## Installation

Switch to the labbox_ephys source directory (cloned above) and open in vscode

```
cd labbox_ephys
code .
```

Install the following vscode extension: ms-vscode-remote.remote-containers

There will be a green button in the lower-left part of the vscode window. Click on that and select the "reopen in container".

This will begin building a docker image and open the development environment inside the container. See the .devcontainer directory for information about exactly what is being installed in the container.

**Important:** If environment variables or the content of the .devcontainer have changed, you will also need to rebuild the container. As mentioned above, you must log out of the operating system and then back in again if environment variables have changed.

## Install the GUI within the container

Use `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac) to open the vscode command window and then run the `Run Task` command. You will see a list of development tasks.

Each time you open the reopen the development environment in the vscode container, you will need to rebuild the application by running the `build-gui` task. Or if not much has changed in the source code, the `build-gui-short` may be all that is needed.

To start the system application in development mode, run the the following services:
* `gui`
* `compute-resource`
* `jupyterlab`

## Open the GUI in a browser

Point google chrome to `http://localhost:5001/app/labbox_ephys`

where 5001 can be replaced by the $LABBOX_EPHYS_PORT chosen above

## To develop individual widgets

First run the task: `gui-install-dev`

Then run the task: `gui-start-dev`

Then open a web browser to `http://localhost:5050`

Open `labbox_ephys_widgets/dev_widget.json`
