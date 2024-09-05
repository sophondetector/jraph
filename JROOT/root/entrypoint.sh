#!/usr/bin/env bash

./prov-deps.sh
./prov-users.sh
./prov-msql-server.sh
./test-sqlcmd.sh

