#!/usr/bin/env python3
import re
import numpy as np
import numpy.typing as npt

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from alive_progress import alive_bar
from PIL import Image
from functools import partial

from src.parsers import points as pointsImporter
from src.parsers import detections as cellImporter
from src.parsers import sampleArea as sampleAreaImporter

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

def importDataset(mask_file: Path, root: Path) -> list[dt.Comparison]:
    """
    Imports and creates all possible datasets associated with a mask file.

    Parameters:
        mask_file: Mask file to use in dataset
        root: The path to look in for data to import
    Returns: A list of import dataset objects
    """

    jobs: list[dt.Comparison] = []

    # Parse model info
    mask_file_regex = re.compile(
        r"(?P<image>.+?)\.ome\.tif\s*-\s*Image\d*\s*_?(?P<model>.+?)_label\.tif"
    )

    mask_file_regex_matches = mask_file_regex.search(mask_file.name)

    if not mask_file_regex_matches:
        raise ValueError(f"Unrecognized format: {mask_file.name}")

    image_name = mask_file_regex_matches.group("image")
    model_name = mask_file_regex_matches.group("model")

    # Parse data from mask
    cell_objects: dict[int, dt.Cell] = cellImporter.tif.parse(str(mask_file.absolute()))
    mask_array: npt.NDArray[np.uint16] = np.array(Image.open(str(mask_file.absolute())), dtype="uint16")

    # Find all points files associated with mask
    points_file_regex = re.compile(
        rf"^{re.escape(image_name)}\.ome\.tif - Image\d*\.geojson$"
    )

    points_files = [
        p for p in root.rglob("*.geojson")
        if p.is_file() and points_file_regex.match(p.name)
    ]

    # Each points file
    for points_file in points_files:
        filepath: str = str(points_file.absolute())

        # Parse data from geojson file
        sample_area: dt.SampleArea = sampleAreaImporter.geojson.parse(filepath)
        points: list[dt.Point] = pointsImporter.geojson.parse(filepath)

        # Construct metadata
        metadata: dt.Metadata = dt.Metadata(image_name, model_name, points_file.name, mask_file.name)

        # Construct job
        jobs.append(dt.Comparison(
            metadata=metadata,
            cells=cell_objects,
            points=points,
            mask=mask_array,
            sample_area=sample_area
        ))

    return jobs

def processJob(mask_file: Path, root: Path, output_directory: Path) -> None:
    """
    Fully imports and processes one job.

    Parameters:
        mask_file: Mask file to process
        root: Path to where files should be imported from
        output_directory: Path to where output files should be stored
    """
    # Build the job object(s)
    datasets: list[dt.Comparison] = importDataset(mask_file, root)

    for data in datasets:
        for process in processing_pipeline:
            data = process.run(data)

        for output in output_pipeline:
            output.run(data, output_directory)

def run(root_dir: str, output_dir: str | None = None, max_workers: int = 4) -> None:
    """
    Run the program

    Parameters:
        root_dir: Path to where to look for file when importing
        output_dir: Path to where output files should be stored
    """
    root_path: Path = Path(root_dir)

    print(f"Workers: {max_workers}")

    output_path: Path = Path(root_path.parent / "Results")
    if output_dir:
        output_path = Path(output_dir)


    mask_filepaths: list[Path] = list(root_path.rglob("*.tif"))

    with alive_bar(len(mask_filepaths), title="Processing Data") as bar:
        with ProcessPoolExecutor(max_workers) as pool:
            job = partial(processJob, root=root_path, output_directory=output_path)
            for _ in pool.map(job, mask_filepaths):
                bar()
