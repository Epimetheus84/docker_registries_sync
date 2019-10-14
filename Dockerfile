FROM ubuntu:18.04

ENV LANG C.UTF-8

# thanks to https://hub.docker.com/r/jpetazzo/dind/dockerfile
RUN apt-get clean && apt-get update -qq && apt-get install -qqy \
    python3 \
    python3-pip \
    build-essential \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://get.docker.com/ | sh

COPY . /srv/flask_app
WORKDIR /srv/flask_app

ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

VOLUME /var/lib/docker

RUN pip3 install -r requirements.txt --src /usr/local/src

##### certificates
COPY certs/ca.crt /usr/local/share/ca-certificates/ca.crt

RUN update-ca-certificates

ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/ca.crt
#####

RUN chmod +x ./start.sh
CMD ["./start.sh"]



