#!/usr/bin/env python3

import numpy as np
import numpy.typing as npt

from dataclasses import dataclass, field

from src.datatypes import Cell, Metadata, Point, Results, SampleArea

@dataclass
class Sample:
    """
    Contains all the data need to process one sample.

    Attributes:
        metadata: Information about the current sample.
        cells: Dictionary of all the cell regions in the sample.
        points: List of all the manually places points in the sample.
        mask: Labeled cell mask to assess.
        original_image: (Optional) Image the mask was generated for.
    """
    metadata: Metadata
    cells: dict[int, Cell]
    points: list[Point]
    mask: npt.NDArray[np.uint16]
    sample_area: SampleArea
    original_image: npt.NDArray[np.uint16] | None = None
    results: Results = field(default_factory=Results)

    # Sets the original_image value to an all black image the same shape as the mask if none is provided.
    def __post_init__(self) -> None:
        if self.original_image is None:
            self.original_image = np.zeros_like(self.mask)
