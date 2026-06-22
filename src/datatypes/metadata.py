#!/usr/bin/env python3

from dataclasses import dataclass
from pandas import Timestamp
import numpy as np
import uuid

@dataclass
class Metadata:
    """
    Holds metadata about a sample.

    Attributes:
        image_name: Name of the sample image.
        model_name: Name of the model that generated the segmentation mask.
        points_file: Name of the file containing ground truth points.
        mask_file: Name of the labeled mask file.
        uuid: Unique identifier for sample.
        timestamp: Time the sample was imported into the program.
    """
    image_name: str = ""
    model_name: str = ""
    points_file: str = ""
    mask_file: str = ""
    uuid: str = str(uuid.uuid1())
    timestamp: Timestamp = Timestamp.now()
