# jraph Data Model and Model Service 
The name `jraph` is a hip, edgy, fun combination of "Jon" and "graph", which sounds like "giraff."
`jraph` is a containerized service that implements the `jraph` data model and provides the ability to create `.kml` files from said `jraph` data model.

## jraph Model
The `jraph` data model is a *directed* graph data model. 
`jraph` intends to be (1) integrable with `Google Earth` and `Analyst Notebook`; and (2) intuitive to extend.
`jraph` intends to make it easy for a group of analysts working from a `jraph` dataset to create `kml` files for viewing in `Google Earth`, in a manner that accomidates "improvised nosql property additions". 
`jraph` is a data model implemented for `Transact SQL` for use with `Microsoft SQL Server`.
`jraph` can also be thought of as "intuitive middleware" for a graph database in TSQL on the right, and Google Earth/Analyst Notebook on the left.
`jraph` is meant to make extensive use of `Transact SQL`'s `nosql`-esque properties.
That is, the formal `jraph` schema will stay very small, containing Lat/Long, integer id, name, and an array of connection ids.

## jraph service MVP
The `jraph` service will have two basic aspects. 
The first is a running `sqlserver` instance, hosting a database which implements the `jraph model` with some model data.
The second aspect is a `python` script which takes a posted list of ids and returns an `output.kml` file.
To communicate with the `jraph` service the client will pass a list of ids into a query string e.g. `https://jraph-service-url.tld/?node_ids=1,3,4`
The user should receive back an `output.kml` file, which the user can then load into `Google Earth`. 
The `output.kml` will show the entity locations on the globe, the connections between them, and the label of the connections between them.

## Dev Basics
* `ndev` contains shell commands and most config variables at the top
* `portal/` is a shared dir between the host dev env and the running service
* `portal/` is shared with a local dev container, and `./ndev push_prod` pushes local changes to `prod`
* `secrets.env` is for passwords, `secrets.env.EXAMPLE` is for `.git`

### Building and Running Jraph Service Locally
```sh
cp secrets.env.EXAMPLE secrets.env
# enter values into secrets.env
./ndev build # build the service
./ndev start # start the service
./ndev shell # open a shell in the service container
```

