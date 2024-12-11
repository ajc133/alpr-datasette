#!/bin/bash
set -eu -o pipefail

source .venv/bin/activate

db_file="osm.db"
api_data_file="overpass.json"
sqlite-utils insert "${db_file}" nodes "${api_data_file}" --truncate --flatten --alter --pk=id
