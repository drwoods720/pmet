#!/usr/bin/env python3

import skimage as ski
import numpy as np
from PIL import Image

import src.datatypes as dt

def parse(filepath: str) -> dict[int, dt.Cell]:
    """
    Generates a dictionary of cell objects from a labeled mask.

    Parameters:
        filepath: Path to the tif file to parse.
    Returns: A dictionary of cell objects.
    """
    mask_image = np.array(Image.open(filepath))

    regions = ski.measure.regionprops(mask_image)

    cells: dict[int, dt.Cell] = {}
    for region in regions:
        cells[region.label] = dt.Cell(region.label)

    return cells
