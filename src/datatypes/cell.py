#!/usr/bin/env python3

from dataclasses import dataclass, field
from .point import Point

@dataclass
class Cell:
    """
    Represents one cell region in the segmentation mask.

    Attributes:
        id: Cell ID. Matches with the cell label in segmentation mask.
        points: List of points that are located within the cell area.
    """
    id: int
    points: list[Point] = field(default_factory=list)
    clipping: bool = False
