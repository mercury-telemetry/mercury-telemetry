FROM raspbian/stretch

ENV PYTHONUNBUFFERED 1

# install common build dependencies and clean up afterwards
RUN apt-get update && apt-get install -y --no-install-recommends \
    raspi-config \
    python3-pip \
    python3-sense-emu \
    sense-emu-tools \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir ~/Downloads
RUN mkdir hardware

# copy setup scripts
COPY ./hardware/setup/raspberrypi-common.sh .

# run setup
RUN bash ./raspberrypi-common.sh

COPY ./hardware/pi_requirements.txt .
RUN sudo python3 -m pip install pip --upgrade --force
RUN sudo pip3 install -r pi_requirements.txt

COPY ./hardware hardware/

CMD [ "python3", "-m", "hardware.main" ]