import json
import requests

from pathlib import Path
from sqlite_utils import Database
from typing import Any

OUT_FILE = "overpass.json"


def fetch_points(bounding_box: str) -> list[Any]:
    query = f"""[out:json][bbox:{bounding_box}];
    node["man_made"="surveillance"]["surveillance:type"="ALPR"];
    out body;>;out skel qt;"""

    result = requests.post(
        "https://overpass-api.de/api/interpreter", data="data=" + query
    )

    data = result.json()
    return data["elements"]


def main():
    # bbox = "37.57597734448728,-122.41782188415529,37.61644104965541,-122.35743999481203"
    bbox = "36.2998674878255,-124.29920384143831,38.889122664457226,-120.43476292346956"
    if not Path(OUT_FILE).exists():
        points = fetch_points(bbox)
        with open(OUT_FILE, "w") as f:
            json.dump(points, f)


if __name__ == "__main__":
    main()
