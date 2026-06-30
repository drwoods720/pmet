#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Point:
    """
    Represents a single manually placed point.

    Attributes:
        x: x coordinate of point
        y: y coordinate of point
        cell: ID of the cell the point is located in. 0 means it isn't located in a cell region.
    """
    x: int
    y: int
    cell: int = 0
