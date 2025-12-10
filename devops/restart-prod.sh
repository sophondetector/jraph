#! /usr/bin/env bash

if [[ $USER != "root" ]]; then 
  printf "this script must be run as root\n";
  exit 1
fi

systemctl restart jraph-app.service
systemctl status jraph-app.service
