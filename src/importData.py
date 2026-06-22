#!/usr/bin/env python3

import re
import numpy as np
import numpy.typing as npt

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from PIL import Image
from alive_progress import alive_bar

import src.datatypes as dt

from src.parsers import points as pointsImporter
from src.parsers import detections as cellImporter
from src.parsers import sampleArea as sampleAreaImporter

def importDataset(mask_file: Path, root: Path) -> list[dt.Comparison]:
    """
    Imports and creates all possible datasets associated with a mask file.

    Parameters:
        mask_file: Mask file to use in dataset
        root: The path to look in for data to import
    """

    jobs: list[dt.Comparison] = []

    # Parse metadata from filename
    image_name: str = mask_file.name.split(".")[0]
    model_name: str = mask_file.name.split("_")[-2]

    # Parse data from mask
    cell_objects: dict[int, dt.Cell] = cellImporter.tif.parse(str(mask_file.absolute()))
    mask_array: npt.NDArray[np.uint16] = np.array(Image.open(str(mask_file.absolute())), dtype="uint16")

    # Find all points files associated with mask
    points_file_regex = re.compile(
        rf"^{re.escape(image_name)}\.ome\.tif - Image\d+\.geojson$"
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

        # Construct and yield job
        jobs.append(dt.Comparison(
            metadata,
            cell_objects,
            points,
            mask_array,
            sample_area
        ))

    return jobs

def importData(root_path: str, multithreaded: bool):
    """
    Creates a list of datasets from a directory of files.

    Parameters:
        root_path: Root path of the data files
        multithreaded: Whether or not paralell processing should be enabled
    """

    root = Path(root_path)

    jobs: list[dt.Comparison] = []

    # Find mask files (files ending in ".tif")
    mask_files: list[Path] = list(root.rglob("*.tif"))

    if not multithreaded:
        with alive_bar(len(mask_files), title="Importing files") as bar:
            for mask in mask_files:
                jobs.extend(importDataset(mask, root))
                bar()
    else:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(importDataset, file, root)
                for file in mask_files
            ]

            with alive_bar(len(futures), title="Importing files") as bar:
                for future in as_completed(futures):
                    try:
                        jobs.extend(future.result())
                    except Exception as e:
                        print("Failed to import dataset", e)
                    finally:
                        bar()
    return jobs
