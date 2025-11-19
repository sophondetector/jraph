#!/usr/bin/env bash

if [[ $USER != "root" ]]; then 
  printf "this script must be run as root\n";
  exit 1
fi

HOST="0.0.0.0"
PORT=443

gunicorn \
  --bind $HOST:$PORT \
  --threads 4 \
  app:app
