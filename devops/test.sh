#!/usr/bin/env bash

# Test command for .sql scripts to be run from the jraph service host machine/container

DB=jongraph
OUTPUT=out.log
INPUT=${1}
PASSWORD=${PASSWORD:-}
SQLUSER=sa

HELP_MESSAGE="$ testSql.sh path/to/input.sql; output in out.log; requires sqlcmd to be installed"

if [[ "$@" =~ \-h\ ? || "$@" =~ \-\-help\ ? ]]; then
	echo $HELP_MESSAGE
	return
fi

echo $DB
echo $OUTPUT
echo $INPUT
echo $PASSWORD
echo $SQLUSER

sqlcmd -C -U $SQLUSER -P $PASSWORD -d $DB -i $INPUT -o $OUTPUT

