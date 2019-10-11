#!/usr/bin/env bash

service nginx start
wrapdocker uwsgi --ini uwsgi.ini
