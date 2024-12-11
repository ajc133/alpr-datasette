import json
import logging
import requests

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)


@dataclass
class BoundingBox:
    south_lat: float
    north_lat: float
    west_lon: float
    east_lon: float

    def __str__(self):
        return f"{self.south_lat},{self.west_lon},{self.north_lat},{self.east_lon}"

    @classmethod
    def from_list(cls, bbox: list[float]):
        assert len(bbox) == 4
        return cls(
            south_lat=bbox[0], north_lat=bbox[1], west_lon=bbox[2], east_lon=bbox[3]
        )


def fetch_bbox(query: str) -> BoundingBox:
    result = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={query}&format=json",
        headers={"user-agent": "Datasette ALPRs"},
    )
    bbox = BoundingBox.from_list(result.json()[0]["boundingbox"])
    logging.debug(f"bbox for {query}: {bbox}")
    return bbox


def fetch_points(bounding_box: BoundingBox) -> list[Any]:
    query = f"""[out:json][bbox:{bounding_box}];
    node["man_made"="surveillance"]["surveillance:type"="ALPR"];
    out body;>;out skel qt;"""
    logging.debug(query)

    result = requests.post(
        "https://overpass-api.de/api/interpreter", data="data=" + query
    )
    result.raise_for_status()

    data = result.json()
    nodes = data["elements"]
    logging.info(f"Received {len(nodes)} nodes")
    return nodes


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-o", "--output", help="Output path for osm data", required=True
    )
    parser.add_argument("query", help="Query that will return a bounding box")
    args = parser.parse_args()

    bbox = fetch_bbox(args.query)

    if not Path(args.output).exists():
        points = fetch_points(bbox)

        with open(args.output, "w") as f:
            json.dump(points, f)
    else:
        logging.info(f"'{args.output}' already exists, skipping download")


if __name__ == "__main__":
    main()
