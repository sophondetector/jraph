#!/usr/bin/env bash


sendSql () {
	HELP_MESSAGE="$ sendSql path/to/input.sql; output in out.log"
	if [[ "$@" =~ \-h\ ? || "$@" =~ \-\-help\ ? ]]; then
		echo $HELP_MESSAGE
		return
	fi

	DB=jongraph
	OUTPUT=out.log
	INPUT=${1}
	PASSWORD='Intrototerror1!'
	SQLUSER=sa
	echo $DB
	echo $OUTPUT
	echo $INPUT
	echo $PASSWORD
	echo $SQLUSER
	sqlcmd -C -U $SQLUSER -P $PASSWORD -d $DB -i $INPUT -o $OUTPUT
}

