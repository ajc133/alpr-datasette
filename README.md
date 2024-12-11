# Deflock Datasette


## Quickstart

### Set up environment
- `./setup.sh`
    - I recommend also reading the script to know what you're installing

### Load database
- `./fetch-osm.sh <region_name>`
    - e.g. `./load-db.sh 'California'`
    - outputs `overpass.json`
- `./load-db.sh`
    - inserts `overpass.json` into `osm.db` sqlite file

### Run datasette

- `./run-db.sh`
