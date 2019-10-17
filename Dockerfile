FROM alpine:latest

COPY . /srv/flask_app
WORKDIR /srv/flask_app

ADD ./wrapdocker /usr/local/bin/wrapdocker
VOLUME /var/lib/docker

# thanks to https://hub.docker.com/r/jpetazzo/dind/dockerfile
RUN apk update \
    && apk add py-pip \
    && apk add bash \
    && apk add docker \
    && pip install --no-cache-dir -r requirements.txt --src /usr/local/src \
    && chmod +x /usr/local/bin/wrapdocker \
    && rm -rf /var/cache/apk/*

##### certificates
COPY certs/ca.crt /usr/local/share/ca-certificates/ca.crt

RUN update-ca-certificates

ENV REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/ca.crt
#####

RUN chmod +x ./start.sh
CMD ["./start.sh"]
