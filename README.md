# jraph and j2k
`jraph` is a basic directed graph data model.

`j2k` is a module which outputs `jraph` data as a `kml` file or as a `gpkg` file.

### Running as a Service
Jraph runs as a `systemd` service named `jraph-app.service`.
To initialize or reinitialize the service, do the following:

1.`cp devops/jraph-app.service /usr/lib/systemd/system`.
1.`systemctl daemon-reload`
1.`systemctl start jraph-app.service`
1.`systemctl status jraph-app.service`


