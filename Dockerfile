FROM raspbian/stretch

# install common build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    raspi-config

RUN echo "Hello, Docker!" > hello.txt