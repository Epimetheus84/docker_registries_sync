#!/usr/bin/env bash

if [ "$NEED_HTTPS" = "true" ]
then

  echo "https enabled"
fi

wrapdocker gunicorn -w 4 index:api --bind 0.0.0.0:80 --timeout 600
