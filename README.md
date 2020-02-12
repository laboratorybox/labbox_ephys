# Labbox-ephys

Browser-based visualization of ephys data

## Installation

### Prerequisites

* Linux
* Docker
* Docker-compose

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

Copy the example config file to the user file

```
cp example_config.user.sh config.user.sh
```

Then edit your config.user.sh which should look something like this:

```
export LOCAL_DATA_DIR=/some/path/to/ephys/data/directory
export KACHERY_STORAGE_DIR=/some/path/to/kachery/storage/directory
export MONGO_DATA_DIR=/some/path/to/mongo/data/directory
export LABBOX_EPHYS_PORT=8080
```

LOCAL_DATA_DIR is a directory where your ephys data are located.

KACHERY_STORAGE_DIR is a directory where the system will store large temporary files.

MONGO_DATA_DIR is a directory where the system will store a persistent database

LABBOX_EPHYS_PORT is the port you will connect to from your web browser

Other variables may also be set in this file (see `config.default.sh` for more information).


### Step 3. Start the services

```
./run_labbox_ephys.sh
```

It may take some time to rebuild the app, depending on the extent of recent changes.

### Step 4. Connect via web browser

Open Google Chrome and enter the following URL (The 8080 should be consistent with LABBOX_EPHYS_PORT set above):

```
http://localhost:8080/app/labbox_ephys
```

If everything worked, you should see some content in the browser

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

