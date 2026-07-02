#!/usr/bin/env python3
"""
processor.py

Defines the :class:`Process` abstract base class, which establishes
the interface that all processors must implement to compute raw
statistics for a sample and return the updated sample data.
"""

from abc import ABC, abstractmethod

import src.datatypes as dt


class Process(ABC):
    """
    Abstract base class for processors.

    Subclasses of :class:`Process` are responsible
    for computing the raw statistics for a sample.
    Each concrete subclass must implement :meth:`run`.
    """

    @abstractmethod
    def run(self, data: dt.Sample) -> dt.Sample: ...
