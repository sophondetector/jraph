#!/usr/bin/env bash

sqlcmd \
	-C \
	-U sa \
	-P $JRAPH_SA_PASSWORD \
	-i test.sql \
	-o out.log

