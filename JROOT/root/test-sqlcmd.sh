#!/usr/bin/env bash

sqlcmd \
	-C \
	-U sa \
	-P $JRAPH_SA_PASSWORD \
	-d jongraph \
	-i test.sql \
	-o out.log

