# Labbox-ephys

Browser-based visualization of ephys data

## Prerequisites

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
export LOCAL_DATA_DIR=[/some/path/to/ephys/data/directory]
export KACHERY_STORAGE_DIR=[/some/path/to/kachery/storage/directory]
export MONGO_DATA_DIR=[/some/path/to/mongo/data/directory]
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
