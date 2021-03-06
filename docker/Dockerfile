FROM ubuntu:18.04

#########################################
### Python                                                               
RUN apt-get update && apt-get -y install git wget build-essential
RUN apt-get install -y python3 python3-pip
RUN ln -s python3 /usr/bin/python
RUN ln -s pip3 /usr/bin/pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-tk

#########################################
### Node 12 and yarn
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && apt-get update && apt-get install -y nodejs
RUN npm install -g yarn

#########################################
### Make sure we have python3 and a working locale
RUN rm /usr/bin/python && ln -s python3 /usr/bin/python && rm /usr/bin/pip && ln -s pip3 /usr/bin/pip
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
RUN apt-get install -y locales && locale-gen en_US.UTF-8

RUN pip install ipython jupyter jupyterlab

RUN mkdir -p /src

#########################################
### Install reactopya
RUN git clone https://github.com/flatironinstitute/reactopya /src/reactopya \
    && cd /src/reactopya \
    && git checkout 8dda2c509f705ce81def848b993ff9517858f645 \
    && pip install -e . \
    && cd reactopya/reactopya_server && yarn install && yarn build && find . -name 'node_modules' -type d -prune -exec rm -rf '{}' + && rm -rf /tmp/* && yarn cache clean

RUN pip install --upgrade setuptools

#########################################
### spikeinterface packages
RUN pip install spikeextractors==0.7.2 spiketoolkit==0.5.2 spikesorters==0.2.5 spikewidgets==0.3.3

#########################################
### Install spikeforest2
RUN git clone https://github.com/flatironinstitute/spikeforest2 /src/spikeforest2 \
    && cd /src/spikeforest2 \
    && git checkout 798775a3dfd7b9147f8503042953134414c31bbb \
    && pip install -e .

### Install spikeforest_widgets
WORKDIR /src/spikeforest2/spikeforest_widgets
RUN reactopya install && find . -name 'node_modules' -type d -prune -exec rm -rf '{}' + && rm -rf /tmp/* && yarn cache clean

### Install labbox_ephys_widgets
COPY labbox_ephys_widgets/reactopya.config.json /src/labbox_ephys_widgets/reactopya.config.json
COPY labbox_ephys_widgets/package.json /src/labbox_ephys_widgets/package.json
COPY labbox_ephys_widgets/widgets /src/labbox_ephys_widgets/widgets
WORKDIR /src/labbox_ephys_widgets
RUN reactopya install && find . -name 'node_modules' -type d -prune -exec rm -rf '{}' + && rm -rf /tmp/* && yarn cache clean

### Install labbox_ephys
COPY labbox_ephys /src/labbox_ephys/labbox_ephys
COPY setup.py /src/labbox_ephys/setup.py
WORKDIR /src/labbox_ephys
RUN pip install .

### Install hither2
RUN git clone https://github.com/laboratorybox/hither2 /src/hither2 \
    && cd /src/hither2 \
    && git checkout 4bb5e1caeb248ebd1f8f1f835f6c64042d68ddb3 \
    && pip install -e .

### Install docker
RUN apt-get update && \
    apt-get -y install apt-transport-https \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
    $(lsb_release -cs) \
    stable" && \
    apt-get update && \
    apt-get -y install docker-ce

### Create the labbox user with sudo privileges - the uid/gid will be changed at runtime
ARG USERNAME=labbox
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME

COPY labbox_ephys_widgets/app /app