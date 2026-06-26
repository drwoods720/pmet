#!/usr/bin/env python3

import numpy as np

import src.datatypes as dt

class DetectClippingCells():
    def run(self, data: dt.Sample) -> dt.Sample:
        """
        Detects all cells that are cut off by the sample area.

        Parameters:
            data: Dataset to process.
        Returns: Processed dataset.
        """
        ymin: int = data.sample_area.ymin
        ymax: int = data.sample_area.ymax
        xmin: int = data.sample_area.xmin
        xmax: int = data.sample_area.xmax

        mask_height, mask_width = data.mask.shape[:2]

        edges = []
        # Original edge pixels (on the boundary)
        edges.append(data.mask[ymin, xmin:xmax+1])
        edges.append(data.mask[ymax, xmin:xmax+1])
        edges.append(data.mask[ymin:ymax, xmin])
        edges.append(data.mask[ymin:ymax, xmax])

        # Pixels behind the clipping line (outside the sample area)
        if ymin > 0:
            edges.append(data.mask[:ymin, xmin:xmax+1])          # above
        if ymax < mask_height - 1:
            edges.append(data.mask[ymax+1:, xmin:xmax+1])        # below
        if xmin > 0:
            edges.append(data.mask[ymin:ymax, :xmin])            # left
        if xmax < mask_width - 1:
            edges.append(data.mask[ymin:ymax, xmax+1:])          # right

        clipping_cells: list[int] = []
        for edge in edges:
            for pixel in edge.flat:  # .flat handles both 1D and 2D arrays
                if pixel != 0 and pixel not in clipping_cells:
                    clipping_cells.append(pixel)

        for cell_id in clipping_cells:
            data.cells[cell_id].clipping = True

        return data
