#!/usr/bin/env bash

HOST="localhost"
PORT=4000

gunicorn \
  --bind $HOST:$PORT \
  --access-logfile=- \
  --log-level debug \
  --reload \
  --reload-extra-file templates/index.html \
  --reload-extra-file static/style.css \
  --reload-extra-file static/jraph.js \
  --reload-extra-file .env \
  app:app
