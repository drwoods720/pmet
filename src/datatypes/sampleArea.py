#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class SampleArea():
    """
    Original sample area.

    Attributes:
        xmax: Maximum x value inside the sample area
        xmin: Minimum x value inside the sample area

        ymax: Maximum y value inside the sample area
        ymin: Minimum x value inside the sample area
    """
    xmax: int
    xmin: int

    ymax: int
    ymin: int
