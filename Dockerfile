FROM ubuntu:latest
RUN  apt-get update 
RUN yes y | apt-get install python3 python3-pip 
RUN python3 --version
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt