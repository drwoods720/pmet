#!/usr/bin/env python3

from typing import override

import pandas as pd

import src.datatypes as dt
from src.parsers.parser import Parser


class Csv(Parser[list[dt.Point]]):
    @override
    def parse(self, filepath: str) -> list[dt.Point]:
        """
        Generates a list of point objects from a csv file.

        Parameters:
        filepath: Path to the csv file to parse.
        Returns: A list of point objects.
        """
        points: list[dt.Point] = []

        dataframe: pd.DataFrame = pd.read_csv(filepath)

        for _, data in dataframe.iterrows():
            point_x: int = int(data["x"])
            point_y: int = int(data["y"])

            point = dt.Point(point_x, point_y)

            points.append(point)

        return points
