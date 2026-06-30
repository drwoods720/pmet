#!/usr/bin/env python3

import json
from typing import override, Any

import src.datatypes as dt
from src.parsers.parser import Parser


class Geojson(Parser[list[dt.Point]]):
    @override
    def parse(self, filepath: str) -> list[dt.Point]:
        """
        Generates a list of point objects from a geojson file.

        Parameters:
        filepath: Path to the geojson file to parse.
        Returns: A list of point objects.
        """
        points: list[dt.Point] = []

        json_data: list[Any] = []
        with open(filepath, "r") as f:
            json_data = json.load(f)

        for feature in json_data:
            if feature["geometry"]["type"] == "MultiPoint":
                for point_entry in feature["geometry"]["coordinates"]:
                    point_x: int = int(point_entry[0])
                    point_y: int = int(point_entry[1])

                    point: dt.Point = dt.Point(point_x, point_y)

                    points.append(point)

        return points
