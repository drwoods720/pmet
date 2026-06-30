#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Results:
    """
    Results of processing calculations.

    Attributes:
        truePositive: Number of true positives.
        falsePositive: Number of false positives.
        falseNegative: Number of false negatives.

        precision: Final precision score.
        recall: Final recall score.
        f1: Final combined precision and recall score.
    """
    truePositive: int = 0
    falsePositive: int = 0
    falseNegative: int = 0

    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
