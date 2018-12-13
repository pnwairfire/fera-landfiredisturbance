FROM ubuntu

ADD . /

RUN apt-get update && apt-get install -y \
wget \
python3 \
python3-pip 

RUN pip3 install pandas
RUN pip3 install requests

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
