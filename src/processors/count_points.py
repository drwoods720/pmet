#!/usr/bin/env python3
"""
count_points.py

Defines the :class:`CountPoints` processor, which assigns each point
to its containing cell and tallies the number of points located
within each cell.
"""

import src.datatypes as dt
from src.processors.processor import Process


class CountPoints(Process):
    """
    Assign points to cells and count points per cell.

    Determines which :class:`~.datatypes.Cell` region each
    :class:`~.datatypes.Point` in the sample falls within, updating
    each point's :attr:`~.datatypes.Point.cell` reference, and
    tallies how many points fall within each cell.
    """

    def run(self, data: dt.Sample) -> dt.Sample:
        """
        Assign each point to its containing cell and count totals.

        :param data: The sample data to process.
        :type data: ~.datatypes.Sample

        :returns: The sample, with each point's
            :attr:`~.datatypes.Point.cell` attribute updated to
            reference its containing cell, and per-cell point counts
            updated accordingly.
        """

        for point in data.points:
            containing_cell_id: int = int(data.mask[point.y, point.x])

            if containing_cell_id > 0:
                point.cell = int(containing_cell_id)
                data.cells[containing_cell_id].points.append(point)

        return data
