#!/usr/bin/env bash

HOST="localhost"
PORT=4000

gunicorn \
  --bind $HOST:$PORT \
  --access-logfile=- \
  --log-level debug \
  --reload \
  app:app
