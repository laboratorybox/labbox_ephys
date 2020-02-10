# Labbox-ephys

Visualization of ephys data

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

### Step 2. Set the environment variables

The following lines can go into your ~/.bashrc file or wherever environment variables are set.

```
export LABBOX_EPHYS_PORT=8080 # Or whichever port you want to use
export KACHERY_STORAGE_DIR=/directory/on/your/machine/for/storing/large/temporary/files
export EPHYS_DATA_DIR=/directory/where/your/ephys/data/lives
```

$LABBOX_EPHYS_PORT is the port you will connect to from your web browser

$KACHERY_STORAGE_DIR is a directory where the system will store large temporary files. 

$EPHYS_DATA_DIR is a directory where your ephys data are located.


### Step 3. Start the services

```
./run_labbox_ephys.sh
```

It may take some time to rebuild the app, depending on the changes.

### Step 4. Connect via web browser

Open Google Chrome and enter the following URL (The 8080 should be consistent with $LABBOX_EPHYS_PORT):

```
http://localhost:8080/app/labbox_ephys
```

If everything worked, you should see some content in the browser
