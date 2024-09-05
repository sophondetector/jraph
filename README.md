# jraph Service
A containerized service that implements the `jraph` data model and the ability to create `.kml` files from said `jraph` data model.
```sh
$ jraph_client /path/to/input-ids.txt
$ cat output.kml
```


## The `jraph` Model
The name `jraph` is a hip, edgy, fun combination of "Jon" and "graph".
The `jraph` data model is a *directed* graph data model. 
`jraph` intends to make it easy for a group of analysts working from a `jraph` dataset to create `kml` files for viewing in `Google Earth`, in a manner that accomidates "improvised nosql property additions". 
`jraph` is a data model implemented for `Transact SQL` for use with `Microsoft SQL Server`.
`jraph` is meant to make extensive use of `Transact SQL`'s `nosql`-esque properties.
That is, the formal `jraph` schema will stay very small, containing Lat/Long, integer id, name, and an array of connection ids.


## First MVP Outline
`jraph` will be a hosted graph database service implemented using `Microsoft SQL Server` and hosted on `Fedora Linux`, and a `.sh` script facilitating interaction with that service.
The `jraph` service will have two basic aspects, the first is a running `sqlcmd` instance, hosting a database which implements a basic graph data model (e.g., the `jraph model`) with some model data (currently in `lib/data.json`); and the second aspect is a `python` script which is in the `cgi-bin` directory which takes a posted list of ids and returns an `output.kml` file.
The user will run a shell script with a single option, the list of entity ids.
The user should be able to submit a list of entity ids (`ents.txt` in the above example) to a remote service and receive back an `output.kml` file, which the user can then load into `Google Earth`. 
The `output.kml` will show the entity locations on the globe, the connections between them, and the nature of the connections between them.


## Dev Set Up
Create a local development container using `podman`. 
This container can then be deployed as a local or cloud service.
Most aspects of the containerd api are eschewed in favor of bash script. 
Any files the container needs are in `JROOT/*`.
`JROOT` is copied over *en toto* during the `podman` build process.


### Configuration
`config.env` is the main configuration file.
`config.EXAMPLE.env` is a version of the configuration file for `.git`, with secret values unfilled.

```sh
cp config.EXAMPLE.env config.env
# enter values into config.env

./ndev.sh build
./ndev.sh start
```

## 0x68 Error
Checking what does mean 0x68 is 104 in decimal, and that is a Connection Reset by Peer error (i.e. the server abruptly closed the connection) and in Linux errors are listed here: https://github.com/torvalds/linux/blob/master/include/uapi/asm-generic/errno.h.
