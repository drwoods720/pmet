#!/usr/bin/env python3
"""
calculate_score.py

Defines the :class:`CalculateScore` processor, which computes
precision, recall, and F1 scores for a sample from its true/false
positive and negative counts.
"""

import src.datatypes as dt
from src.processors.processor import Process


class CalculateScore(Process):
    """
    Calculate scoring metrics for a sample.

    Computes precision, recall, and F1 scores from the sample's
    classification counts, storing them in the sample's
    :class:`~.datatypes.Results`.
    """

    def run(self, data: dt.Sample) -> dt.Sample:
        """
        Calculate and store the scoring metrics for a sample.

        Calculates precision, recall, and F1 scores.

        :param data: The sample data to calculate scores for.
        :type data: ~.datatypes.Sample

        :returns: The sample and its
            :attr:`~.datatypes.Sample.results` updated to include
            the calculated precision, recall, and F1 scores.
        :rtype: ~.datatypes.Sample
        """
        # Count false negatives
        for point in data.points:
            if point.cell < 1:
                data.results.false_negative += 1

        for cell in data.cells.values():
            if cell.clipping:
                continue

            point_count: int = len(cell.points)

            if point_count < 1:
                data.results.false_positive += 1
            elif point_count == 1:
                data.results.true_positive += 1
            elif point_count > 1:
                data.results.true_positive += 1
                data.results.false_negative += point_count - 1

            tp: int = data.results.true_positive
            fp: int = data.results.false_positive
            fn: int = data.results.false_negative

            data.results.precision = round(tp / (tp + fp) if (tp + fp) > 0 else 0.0, 3)
            data.results.recall = round(tp / (tp + fn) if (tp + fn) > 0 else 0.0, 3)
            data.results.f1 = round(
                (2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0.0), 3
            )

        return data
