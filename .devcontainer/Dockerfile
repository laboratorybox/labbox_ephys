FROM ubuntu:18.04

#########################################
### Node 12 and yarn
### best to do this before python
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && apt-get update && apt-get install -y nodejs
RUN npm install -g yarn

#########################################
### Python                                                               
RUN apt-get update && apt-get -y install git wget build-essential
RUN apt-get install -y python3 python3-pip
### Make sure we have python3 and a working locale
RUN (rm /usr/bin/python || true) && ln -s python3 /usr/bin/python && (rm /usr/bin/pip || true) && ln -s pip3 /usr/bin/pip
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
RUN apt-get install -y locales && locale-gen en_US.UTF-8
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-tk

#########################################
### Numpy
RUN pip install numpy

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# This Dockerfile adds a non-root user with sudo access. Use the "remoteUser"
# property in devcontainer.json to use it. On Linux, the container user's GID/UIDs
# will be updated to match your local UID/GID (when using the dockerFile property).
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Uncomment the following COPY line and the corresponding lines in the `RUN` command if you wish to
# include your requirements in the image itself. It is suggested that you only do this if your
# requirements rarely (if ever) change.
# COPY requirements.txt /tmp/pip-tmp/

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git openssh-client less iproute2 procps lsb-release \
    #
    # Install pylint
    && pip --disable-pip-version-check --no-cache-dir install pylint \
    #
    # Update Python environment based on requirements.txt
    # && pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    # && rm -rf /tmp/pip-tmp \
    #
    # Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Let the installed vscode extensions persist between rebuilds
# See: https://code.visualstudio.com/docs/remote/containers-advanced#_avoiding-extension-reinstalls-on-container-rebuild
RUN mkdir -p /home/$USERNAME/.vscode-server/extensions && chown -R $USERNAME /home/$USERNAME/.vscode-server

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# docker
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

RUN pip install ipython jupyter jupyterlab
RUN pip install pymongo

RUN pip install --upgrade setuptools

# for testing display
RUN apt-get install -y gedit

# docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

# spikeinterface packages
RUN pip install spikeextractors==0.7.2 spiketoolkit==0.5.2 spikesorters==0.2.5 spikewidgets==0.3.3

# nano
RUN apt-get install -y nano

# pytest, etc
RUN pip install pylint ipython pytest pytest-cov

# In order to run the electron app:
RUN apt-get install -y libasound2 libnss3-dev

RUN pip install simplejson mpld3

ENV PATH=$PATH:/workspaces/labbox_ephys/bin

RUN /bin/sh -c "usermod -aG docker vscode && newgrp docker"

# RUn apt-get install -y libgtk3.0-cil-dev libgtk2.0.0 libnss3-dev libx11-xcb1
# RUN apt-get install -y libasound2
# RUN npm install -g electron

# #########################################
# ### Install spikeforest2
# RUN git clone https://github.com/flatironinstitute/spikeforest2 /src/spikeforest2 \
#     && cd /src/spikeforest2 \
#     && git checkout 798775a3dfd7b9147f8503042953134414c31bbb \
#     && pip install -e .

# ### Install spikeforest_widgets
# WORKDIR /src/spikeforest2/spikeforest_widgets
# RUN reactopya install && find . -name 'node_modules' -type d -prune -exec rm -rf '{}' + && rm -rf /tmp/* && yarn cache clean

