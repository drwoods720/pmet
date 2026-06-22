#!/usr/bin/env python3

import src.datatypes as dt
import pandas as pd

def parse(filepath: str) -> list[dt.Point]:
    """
    Generates a list of point objects from a tsv file.

    Parameters:
        filepath: Path to the tsv file to parse.
    Returns: A list of point objects.
    """
    points: list[dt.Point] = []

    dataframe = pd.read_csv(filepath, sep="\t")

    for index, data in dataframe.iterrows():
        point_x: int = int(data["x"])
        point_y: int = int(data["y"])

        point = dt.Point(point_x, point_y)

        points.append(point)

    return points
