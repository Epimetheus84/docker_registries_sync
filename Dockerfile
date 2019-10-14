FROM python:3.6-slim

# thanks to https://hub.docker.com/r/jpetazzo/dind/dockerfile
RUN apt-get clean && apt-get update -qq && apt-get install -qqy \
    nginx \
    python3-dev \
    build-essential \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash  \
    && apt-get update

RUN apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://get.docker.com/ | sh

COPY . /srv/flask_app
WORKDIR /srv/flask_app

ADD ./wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

VOLUME /var/lib/docker

RUN cd client && npm i && npm run build && rm -rf node_modules

RUN pip install -r requirements.txt --src /usr/local/src

##### certificates
COPY certs/ca.crt /usr/local/share/ca-certificates/ca.crt

RUN update-ca-certificates

ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/ca.crt
#####

RUN chmod +x ./start.sh
CMD ["./start.sh"]



