#!/usr/bin/env bash

echo "testing sql service"

sqlcmd \
	-C \
	-U sa \
	-P $JRAPH_SA_PASSWORD \
	-d jongraph \
	-i test.sql \
	-o out.log

