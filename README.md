# jraph Service
A containerized service that implements the `jraph` data model and the ability to create `.kml` files from said `jraph` data model.


## The `jraph` Model
The name `jraph` is a hip, edgy, fun combination of "Jon" and "graph".
The `jraph` data model is a *directed* graph data model. 
`jraph` intends to make it easy for a group of analysts working from a `jraph` dataset to create `kml` files for viewing in `Google Earth`, in a manner that accomidates "improvised nosql property additions". 
`jraph` is a data model implemented for `Transact SQL` for use with `Microsoft SQL Server`.
`jraph` is meant to make extensive use of `Transact SQL`'s `nosql`-esque properties.
That is, the formal `jraph` schema will stay very small, containing Lat/Long, integer id, name, and an array of connection ids.


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
The user will run a shell script with a single option, the list of entity ids.
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
* `devops/FILESYSTEM_ROOT/*` contains all the container system and build files; the directory is essentially part of the `jraph` image schema.
* `devops/FILESYSTEM_ROOT/root/` contains all provisioning scripts `prov-*.sh`, which are all packaged together into `/root/entrypoint.sh`.


## Dev Set Up
Create a local development container using `podman`. 
This container can then be deployed as a local or cloud service.
Most aspects of the containerd api are eschewed in favor of bash script. 
Any files the container needs are in `devops/FILESYSTEM_ROOT/*`.
`FILESYSTEM_ROOT` is copied over *en toto* during the `podman` build process.


### Configuration
`devops/config.sh` is the main configuration file.
`devops/config.EXAMPLE.sh` is a version of the configuration file for `.git`, with secret values unfilled.

```sh
cp devops/config.EXAMPLE.sh devops/config.sh # and then enter your desired values

./dev-tools.sh create_jraph_image
./dev-tools.sh test_jraph_image
```

## 0x68 Error
Checking what does mean 0x68 is 104 in decimal, and that is a Connection Reset by Peer error (i.e. the server abruptly closed the connection) and in Linux errors are listed here: https://github.com/torvalds/linux/blob/master/include/uapi/asm-generic/errno.h.
