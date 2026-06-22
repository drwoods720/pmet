#!/usr/bin/env python3

import json

import src.datatypes as dt

def parse(filepath: str) -> list[dt.Point]:
    """
    Generates a list of point objects from a geojson file.

    Parameters:
        filepath: Path to the geojson file.
    Returns: A list of point objects
    """

    # Declare points list
    points: list[dt.Point] = []

    # Load in json data
    json_data = []
    with open(filepath, 'r') as f:
        json_data = json.load(f)


    # Find the correct feature
    for feature in json_data:
        if feature["geometry"]["type"] == "MultiPoint":
            for point in feature["geometry"]["coordinates"]:
                point_x: int = int(point[0])
                point_y: int = int(point[1])

                point: dt.Point = dt.Point(point_x, point_y)

                points.append(point)

    return points
