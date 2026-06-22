#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class Results:
    """
    """
    truePositive: int = 0
    falsePositive: int = 0
    falseNegative: int = 0

    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
