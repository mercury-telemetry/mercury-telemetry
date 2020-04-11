FROM raspbian/stretch

# install common build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    raspi-config \
    && rm -rf /var/lib/apt/lists/*

# copy setup scripts
COPY ./hardware .

# run setup
RUN bash ./setup/raspberrypi-common.sh

RUN echo "Hello, Docker!" > hello.txt