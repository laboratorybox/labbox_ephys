# Labbox-ephys services

| Service            | Purpose            | Where it runs      | Connects to |
| -------------      | -------------      | -------------      | ------------- |
| Database           | Stores recordings/sortings a facilitates communication between services | Clooud                | |
| Kachery server     | Stores large files via SHA1-hash accessible by all services | A computer with large disk, accessible from internet | |
| Compute resource   | Runs spike sorting and other processing | A computer with Disk, RAM, CPU resources | Database, kachery server |
| GUI                | Hosts the web GUI | Locally or in the cloud  | Database, kachery server |
| Jupyter Lab server | Hosts a JupyterLab session for running notebooks | Same machine as GUI | Database, kachery server |
| Processing daemon  | Manages processing of queued spike sorting and other processing | Same machine as GUI | Database, kachery server |
