#!/usr/bin/env python3

import time

import src.datatypes as dt

import src.importData as importData
import src.processor as processor

def run(path: str, multithreaded: bool) -> None:
    """
    Runs the processing pipeline on files from a specific directory.

    Parameters:
        path: Path to input files
        multithreaded: Whether or not to use multithreading
    """

    start_time = time.time()

    jobs: list[dt.Comparison]

    if multithreaded:
        print("Running in threaded mode...")
    else:
        print("Running in normal mode...")

    jobs = importData.importData(path, multithreaded)
    processor.processData(jobs, multithreaded)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Processing complete! Took {elapsed_time:.2f} seconds.")
