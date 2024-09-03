# jraph Service
## Basic Use
```sh
$ cat ents.txt # newline delimited entity ids
1
4
5
2
$ jraph ents.txt
$ cat output.kml
```

## First MVP Outline
`jraph` will be a hosted graph database service implemented using `Microsoft SQL Server` and hosted on `Fedora Linux`, and a `.sh` script facilitating interaction with that service.
The `jraph` service will have two basic aspects, the first is a running `sqlcmd` instance, hosting a database which implements a basic graph data model (e.g., the `jraph model`) with some model data (currently in `lib/data.json`); and the second aspect is a `python` script which is in the `cgi-bin` directory which takes a posted list of ids and returns an `output.kml` file.
The user can run shell scripts with a single option.
The user should be able to submit a list of entity ids (`ents.txt` in the above example) to a remote service and receive back an `output.kml` file, which the user can then load into `Google Earth`. 
The `output.kml` will show the entity locations on the globe, the connections between them, and the nature of the connections between them.

## Further Development
The first client script will be `.sh` and the second client script will be a `powershell` script.
The first hosted service will be built on my home computer using `podman`, and saved as an `image`. 
That container image will then be hosted as a Digital Ocean `droplet`.
The next stage of development will be a basic `html` interface hosted at `jraph.nathanielhtaylor.com`.
The next stage will only commnece **after** the MVP has been completed for `.sh` and `powershell`.
The stage after that will be allowing users to submit sql commands either through `sqlcmd` or the `jraph` tool.
The stage after *that* will be securing the remote droplet.

## File Structure
* `lib/` contains Jon's `sql` and some `sql` scraps which will form the raw material for the first mvp schema.
* `lib/modelSql` contains some model `sql` I got from somewhere.
* `devops/*.sh` contains provisioning scripts for the `jraph` service container.
* `devops/FILESYSTEM_START/*` contains some system files for the `jraph` service container.

