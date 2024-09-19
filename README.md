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

## Dev Basics
* `ndev` contains shell commands and most config variables at the top.
* `./ndev` *without args* will list available ndev functions
* the repo directory is shared with `/root/jraph` in both the local and prod instances
* assume everything is going to be run from `/root`, in other words, write as if you were always going to run from `../`
* `secrets.env` is for passwords, `secrets.env.EXAMPLE` is for `.git`

### Building and Running Jraph Service Locally
```sh
cp secrets.env.EXAMPLE secrets.env
# enter values into secrets.env
./ndev build # build the service
./ndev loc.start.server # start the sql server 
./ndev loc.start # start the jraph service
./ndev loc # open a shell in the service container
```

### Deployng
* Deployed to Digital Ocean
* See `./ndev doc.*` commands
* Currently deployed to `jraph.nathanielhtaylor.com`

### Building Test DB
1. Run `$ python3 -m jtool.init.csv_*.py` in order.
1. Run `$ python3 -m jtool.init.db_*.py` in order.

### TSQL Functions and Admin
* [docs on tsql funcs](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-readerrorlog-transact-sql?view=sql-server-ver16)

