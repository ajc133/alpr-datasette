#!/bin/bash

source ".venv/bin/activate"

api_data_file="overpass.json"
db_file="osm-sfba.db"

python src/deflock_datasette/osm.py --output "${api_data_file}" "California"
sqlite-utils insert "${db_file}" nodes "${api_data_file}" --truncate --flatten --alter --pk=id
sqlite-utils convert "${db_file}" nodes id '{"title": "node/"+str(value)}' --output popup
