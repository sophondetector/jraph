# jraph and j2k
`jraph` is a basic directed graph data model.

`j2k` is a module which outputs `jraph` data as a `kml` file.

## Dev 
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

