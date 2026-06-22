#!/usr/bin/env python3

from concurrent.futures import ProcessPoolExecutor, as_completed
from alive_progress import alive_bar

import src.processors as processors
import src.outputs as outputs

import src.datatypes as dt

# Ordered list of processing steps that will be run on the data
processing_pipeline = [
    processors.CountPoints(),
    processors.DetectClippingCells(),
    processors.CalculateScore(),
]

# Ordered list of output steps that will be run on the data
output_pipeline = [
    outputs.ScoresCsv(),
    outputs.Overlay(),
]

def processJob(data: dt.Comparison) -> None:
    """
    Preforms the entire processing pipeline on a single dataset

    Parameters:
        data: Data to process
    """

    # Processing steps
    for process in processing_pipeline:
        data = process.run(data)

    # Output steps
    for output in output_pipeline:
        output.run(data)

def processData(datasets: list[dt.Comparison], multithreaded: bool) -> None:
    """
    Preforms the processing and output pipelines on every dataset in a list of datasets.

    Parameters:
        datasets: List of datasets to process
        multithreaded: Whether or not paralell processing should be enabled
    """
    if not multithreaded:
        with alive_bar(len(datasets), title="Processing data") as bar:
            for dataset in datasets:
                processJob(dataset)
                bar()
    else:
        with ProcessPoolExecutor() as pool:
            futures = [pool.submit(processJob, dataset) for dataset in datasets]

            with alive_bar(len(datasets), title="Processing data") as bar:
                for future in as_completed(futures):
                    bar()
