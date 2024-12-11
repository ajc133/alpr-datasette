#!/bin/bash
set -eux -o pipefail

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/datasette install datasette-cluster-map
