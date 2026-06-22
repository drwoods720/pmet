#!/usr/bin/env python3
import src.datatypes as dt

class CountPoints():
    def run(self, data: dt.Comparison) -> dt.Comparison:
        """
        Determines which cell a point is in and how many points are in each cell.

        Parameters:
            data: Sample data to process
        Returns: Sample data with updated point counts
        """
        for point in data.points:
            containing_cell_id: int = int(data.mask[point.y, point.x])

            if containing_cell_id > 0:
                point.cell = int(containing_cell_id)
                data.cells[containing_cell_id].points.append(point)

        return data
