#!/usr/bin/env python3

from typing import override

import skimage as ski
import numpy as np
import numpy.typing as npt
from PIL import Image

import src.datatypes as dt
from src.parsers.parser import Parser


class Tif(Parser[dict[int, dt.Cell]]):
    @override
    def parse(self, filepath: str) -> dict[int, dt.Cell]:
        """
        Generates a dictionary of cell objects from a labeled mask.

        Parameters:
        filepath: Path to the tif file to parse.
        Returns: A dictionary of cell objects.
        """
        mask_image: npt.NDArray[np.uint16] = np.array(
            Image.open(filepath), dtype="uint16"
        )

        cell_regions = ski.measure.regionprops(mask_image)

        cells: dict[int, dt.Cell] = {}
        for region in cell_regions:
            cells[region.label] = dt.Cell(region.label)

        return cells
