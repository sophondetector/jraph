#! /usr/bin/env bash

if [[ $USER != "root" ]]; then 
  printf "this script must be run as root\n";
  exit 1
fi

printf "restarting jraph-app.service..."
systemctl restart jraph-app.service
printf "done"
systemctl status jraph-app.service
