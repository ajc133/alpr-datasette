#!/bin/bash
set -eu -o pipefail

source .venv/bin/activate
api_data_file="overpass.json"
if [[ $# -ne 1 ]]; then
	# the nominatim bounds are buggy if you do too big of a region :)
	echo "Usage: $0 <region_name>" >&2
	exit 1
fi
region_name="$1"

python src/deflock_datasette/osm.py --output "${api_data_file}" "$region_name"
