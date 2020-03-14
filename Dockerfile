FROM raspbian/stretch

# install common build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    raspi-config

# copy setup scripts
COPY ./hardware/setup .

# run setup
RUN bash raspberrypi-common.sh

RUN echo "Hello, Docker!" > hello.txt