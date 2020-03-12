FROM ubuntu:18.04

#########################################
### Python                                                               
RUN apt-get update && apt-get -y install git wget build-essential
RUN apt-get install -y python3 python3-pip
RUN ln -s python3 /usr/bin/python
RUN ln -s pip3 /usr/bin/pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-tk

# packages
RUN pip install matplotlib mpld3

#########################################
### spikeinterface packages
RUN pip install spikeextractors==0.7.2 spiketoolkit==0.5.2 spikesorters==0.2.5 spikewidgets==0.3.3

# Not sure why we need this
RUN pip install jinja2