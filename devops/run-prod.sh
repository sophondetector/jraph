#!/usr/bin/env bash

if [[ $USER != "root" ]]; then 
  printf "this script must be run as root\n";
  exit 1
fi

HOST="0.0.0.0"
PORT=80
THREADS=4

gunicorn \
  --bind $HOST:$PORT \
  --threads $THREADS \
  app:app
