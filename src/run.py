#!/usr/bin/env python3

import time

from collections.abc import Iterable

import src.datatypes as dt

import src.main as main

def run(path: str) -> None:
    """
    Runs the processing pipeline on files from a specific directory.

    Parameters:
        path: Path to input files
    """

    start_time = time.time()

    main.run(path)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Processing complete! Took {elapsed_time:.2f} seconds.")
