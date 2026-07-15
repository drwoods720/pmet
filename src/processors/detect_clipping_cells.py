#!/usr/bin/env python3
"""
detect_clipping_cells.py

Defines the :class:`DetectClippingCells` processor, which flags
cells that are cut off by the boundry of the sample area.
"""

import src.datatypes as dt
from src.processors.processor import Process

import numpy as np
import numpy.typing as npt

class DetectClippingCells(Process):
    """
    Detect cells that are clipped by the sample area boundary.

    Marks each cell in the sample whose region is cut off by the
    edge of the :class:`~.datatypes.SampleArea`, by setting its
    :attr:`~.datatypes.Cell.clipping` attribute accordingly.
    """

    def run(self, data: dt.Sample) -> dt.Sample:
        """
        Detect and flag all cells clipped off by the sample area.

        :param data: The sample data to process.
        :type data: ~.datatypes.Sample

        :returns: The sample, with each cell's
            :attr:`~.datatypes.Cell.clipping` attribute updated to
            reflect whether it is cut off by the sample area
            boundary.
        :rtype: ~.datatypes.Sample
        """
        ymin: int = data.sample_area.ymin
        ymax: int = data.sample_area.ymax
        xmin: int = data.sample_area.xmin
        xmax: int = data.sample_area.xmax

        outside_mask: npt.NDArray[bool] = np.ones(data.mask.shape, dtype=bool)
        outside_mask[ymin:ymax + 1, xmin:xmax +1] = False

        clipping_cells: list[int] = set(data.mask[outside_mask])
        clipping_cells.discard(0)

        for cell_id in clipping_cells:
            data.cells[cell_id].clipping = True

        return data
