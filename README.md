[![Build Status](https://travis-ci.org/laboratorybox/labbox_ephys.svg?branch=master)](https://travis-ci.org/laboratorybox/labbox_ephys)
[![codecov](https://codecov.io/gh/laboratorybox/labbox_ephys/branch/master/graph/badge.svg)](https://codecov.io/gh/laboratorybox/labbox_ephys)

[![license](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Python](https://img.shields.io/badge/python-%3E=3.6-blue.svg)

# Labbox-ephys

Browser-based visualization and processing of ephys data. We are at the prototyping stage.

## Installation

### Prerequisites

* Linux
* Docker
* Docker-compose
* Chrome web browser

It is important that you are able to run docker as a regular (non-root) user. To enable this, you must add your user to the docker group as follows:

```
sudo usermod -aG docker vscode
newgrp docker
```

Now verify that you can run docker without sudo:

```
docker run hello-world
```

### Step 1. Clone this repository

```
git clone https://github.com/laboratorybox/labbox_ephys
cd labbox_ephys
```

Subsequently, for updates:

```
cd labbox_ephys
git pull
```

### Step 2. Configuration

Set the following environment variables at the bottom of your `~/.bashrc` file (after editing this file you will either need to log in again or open a new terminal):

```
# An existing directory where the system will store large temporary files.
export KACHERY_STORAGE_DIR=/some/path/to/kachery-storage

# The port you will connect to from your web browser
export LABBOX_EPHYS_PORT=8080

# The port you will connect to jupyterlab from your web browser
export LABBOX_EPHYS_JUPYTERLAB_PORT=8891

# An existing directory where your ephys data are located.
export LABBOX_EPHYS_DATA_DIR=/some/path/to/local-data

# An existing directory where the system will store a persistent database
export LABBOX_EPHYS_MONGO_DATA_DIR=/some/path/to/mongo-data

# The path to the source directory (where you cloned labbox_ephys)
export LABBOX_EPHYS_SOURCE_DIR=/path/to/the/source/directory/of/labbox_ephys
```

It is important that all of these directories already exist and have read/write privileges by the current user.

### Step 3. Start the services

```
cd docker
./run_labbox_ephys.sh
```

It may take some time to rebuild the app, depending on the extent of recent changes.

### Step 4. Connect via web browser

Open Google Chrome and enter the following URL (The 8080 should be consistent with LABBOX_EPHYS_PORT set above):

```
http://localhost:8080/app/labbox_ephys
```

If everything worked, you should see some content in the browser.

### Step 5. Connect from a different computer within the internal network

Depending on your network configuration, you should be able to connect from a different computer within your internal network by replacing localhost above by the ip address of the linux box running the server.

## Importing recordings

From the main labbox_ephys page, click on "Open JupyterLab" to open a new browser tab running JupyterLab. This is a JupyterLab session inside the labbox. It gives you direct access to files within the labbox and allows you to run Python code using notebooks (.ipynb files). [Click here for more information about JupyterLab](https://jupyterlab.readthedocs.io/en/stable/#).

You should see two folders on the left: "local-data" and "example_notebooks". The local-data folder corresponds to the LOCAL_DATA_DIR specified above. The example_notebooks directory is a read-only directory of example Jupyter notebooks to help get you started.

### Importing example SpikeForest recordings

To download and import some example recordings from the SpikeForest database, double-click on `example_notebooks` and then on `example_spikeforest_import.ipynb`. This will open a notebook that will allow you to import some example recordings from the SpikeForest database. If you run the notebook cells it will download and import the data. Depending on the speed of your internet connection, it may take some time to download the data (a few gigabytes).

Once the recordings are imported, you can then go back to the main labbox_ephys page and click on the "View recordings" link. You should then be able to see the imported recordings.

### Importing recordings from disk

To import recordings from disk, first save your recordings in individual directories inside the $LOCAL_DATA_DIR directory. Right now only the `raw.mda` format is supported, but this will soon expand to include other formats. The directory names will be used as the recording IDs during import. You may want to use a nested directory structure to achieve a hierarchical organization of the recordings.

From within JupyterLab, open the `example_notebooks/example_local_import.ipynb` notebooks and run the notebook cells. This will automatically find and import all of the recordings found in the the $LOCAL_DATA_DIR directory.

Once the recordings are imported, you can then go back to the main labbox_ephys page and click on the "View recordings" link. You should then be able to see the imported recordings.

### Spike sorting

There is also an example notebook for performing preliminary spike sorting. The results of the spike sorting get inserted into the database and may be visualized through the web interface.

## Flatiron probe file format (.json)
 
See [probe_files/README.md](probe_files/README.md)
