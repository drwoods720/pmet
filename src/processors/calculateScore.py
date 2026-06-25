#!/usr/bin/env python3

import src.datatypes as dt

class CalculateScore():
    def run(self, data: dt.Comparison) -> dt.Comparison:
        """
        Calculates the scoring metrics from a specific dataset.

        Will calculate precision, recall, and f1 scores.

        Parameters:
            data: Dataset to calculate scores for.
        Returns: Dataset with scores added.
        """
        # Count false negatives
        for point in data.points:
            if point.cell < 1:
                data.results.falseNegative += 1

        for cell in data.cells.values():
            if cell.clipping:
                continue

            point_count: int = len(cell.points)

            if point_count < 1:
                data.results.falsePositive += 1
            elif point_count == 1:
                data.results.truePositive += 1
            elif point_count > 1:
                data.results.truePositive += 1
                data.results.falseNegative += point_count - 1

            tp: int = data.results.truePositive
            fp: int = data.results.falsePositive
            fn: int = data.results.falseNegative

            data.results.precision = round(tp / (tp + fp) if (tp + fp) > 0 else 0.0, 3)
            data.results.recall = round(tp / (tp + fn) if (tp + fn) > 0 else 0.0, 3)
            data.results.f1 = round((
                2 * tp / (2 * tp + fp + fn)
                if (2 * tp + fp + fn) > 0
                else 0.0
            ), 3)

        return data
