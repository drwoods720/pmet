#!/usr/bin/env python3
"""
detectClippingCells.py

Defines the :class:`DetectClippingCells` processor, which flags
cells that are cut off by the boundry of the sample area.
"""

import src.datatypes as dt
from src.processors.processor import Process


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

        mask_height, mask_width = data.mask.shape[:2]

        edges = []
        # Original edge pixels (on the boundary)
        edges.append(data.mask[ymin, xmin : xmax + 1])
        edges.append(data.mask[ymax, xmin : xmax + 1])
        edges.append(data.mask[ymin:ymax, xmin])
        edges.append(data.mask[ymin:ymax, xmax])

        # Pixels behind the clipping line (outside the sample area)
        if ymin > 0:
            edges.append(data.mask[:ymin, xmin : xmax + 1])  # above
        if ymax < mask_height - 1:
            edges.append(data.mask[ymax + 1 :, xmin : xmax + 1])  # below
        if xmin > 0:
            edges.append(data.mask[ymin:ymax, :xmin])  # left
        if xmax < mask_width - 1:
            edges.append(data.mask[ymin:ymax, xmax + 1 :])  # right

        clipping_cells: list[int] = []
        for edge in edges:
            for pixel in edge.flat:  # .flat handles both 1D and 2D arrays
                if pixel != 0 and pixel not in clipping_cells:
                    clipping_cells.append(pixel)

        for cell_id in clipping_cells:
            data.cells[cell_id].clipping = True

        return data
