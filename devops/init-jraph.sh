#!/usr/bin/env sh

if [[ ! -v JRAPH_SA_PASSWORD ]]; then
	echo "\$JRAPH_SA_PASSWORD required!"
	exit 1
fi

echo "initializing jraph database"
sqlcmd -C -U sa -P $JRAPH_SA_PASSWORD -i lib/sql/jraph-schema.sql 

echo "inserting nodes"
sqlcmd -C -U sa -P $JRAPH_SA_PASSWORD -d jraph -i lib/sql/jraph-init-nodes.sql 

echo "inserting edges"
sqlcmd -C -U sa -P $JRAPH_SA_PASSWORD -d jraph -i lib/sql/jraph-init-edges.sql 

echo "jraph database init finito"
