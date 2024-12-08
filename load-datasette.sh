#!/bin/bash

source ".venv/bin/activate"

python src/deflock_datasette/osm.py
sqlite-utils insert osm-sfba.db nodes overpass.json --truncate --flatten --alter --pk=id
sqlite-utils convert osm-sfba.db nodes id '{"title": "node/"+str(value)}' --output popup
datasette install datasette-cluster-map 
datasette osm-sfba.db