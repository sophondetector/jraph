# jraph Data Model and Model Service 
A containerized service that implements the `jraph` data model and provides the ability to create `.kml` files from said `jraph` data model.
```sh
$ ./ndev.sh start & # start the jraph service
$ jraph_client /path/to/input-ids.txt
$ cat output.kml
```

## Dev Set Up
* `portal/` is a shared dir between the host repo and the local dev container `/root/portal`.
* `config.env` is the main configuration file.
* `config.env.EXAMPLE` is a version of the configuration file for `.git`, with secret values unfilled.

### Building and Running Jraph Service Locally
```sh
cp config.env.EXAMPLE config.env
# enter values into config.env

./ndev.sh build
./ndev.sh start 
./ndev.sh shell # in a separate window
```

## jraph Model
The name `jraph` is a hip, edgy, fun combination of "Jon" and "graph".
The `jraph` data model is a *directed* graph data model. 
`jraph` intends to make it easy for a group of analysts working from a `jraph` dataset to create `kml` files for viewing in `Google Earth`, in a manner that accomidates "improvised nosql property additions". 
`jraph` is a data model implemented for `Transact SQL` for use with `Microsoft SQL Server`.
`jraph` is meant to make extensive use of `Transact SQL`'s `nosql`-esque properties.
That is, the formal `jraph` schema will stay very small, containing Lat/Long, integer id, name, and an array of connection ids.

## jraph service MVP
`jraph` will be a hosted graph database service implemented using `Microsoft SQL Server` and hosted on `Fedora Linux`, and a `.sh` script facilitating interaction with that service.
The `jraph` service will have two basic aspects, the first is a running sqlserver instance, hosting a database which implements the `jraph model` with some model data (currently in `lib/data.json`); and the second aspect is a `python` script which is in the `cgi-bin` directory which takes a posted list of ids and returns an `output.kml` file.
To communicate with the `jraph` service, the client (e.g., the user) will run a shell script with a single option, the list of entity ids.
The user should be able to submit a list of entity ids to the `jraph` service and receive back an `output.kml` file, which the user can then load into `Google Earth`. 
The `output.kml` will show the entity locations on the globe, the connections between them, and the label of the connections between them.

## Notes
### 0x68 Error
Checking what does mean 0x68 is 104 in decimal, and that is a Connection Reset by Peer error (i.e. the server abruptly closed the connection) and in Linux errors are listed here: https://github.com/torvalds/linux/blob/master/include/uapi/asm-generic/errno.h.
