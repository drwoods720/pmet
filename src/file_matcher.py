#!/usr/bin/env python3

import re
from pathlib import Path


ANNOTATION_FILE_REGEX: re.Pattern[str] = re.compile(
    rf"^(?P<image_name>.*?)\.ome\.tif( - Image(?P<image_index>\d+)?)?.geojson$"
)


def find_associated_mask_files(root: Path, image_name: str) -> list[tuple[Path, str]]:
    MASK_FILE_REGEX: re.Pattern[str] = re.compile(
        rf"^(?P<image_name>{image_name})\.ome\.tif - (Image(?P<image_index>\d+)?)? ?(?P<model_name>.*?)_label\.tif$"
    )

    associated_mask_files: list[tuple[Path, str]] = []

    for mask_file in root.rglob("*.tif"):
        re_match: re.Match[str] | None = MASK_FILE_REGEX.match(mask_file.name)


        if not mask_file.is_file() or not re_match:
            continue

        model_name: str = re_match.groupdict()["model_name"]

        associated_mask_files.append((mask_file, model_name))

    return associated_mask_files

def associate_files(root: Path) -> dict[tuple[Path, str], list[tuple[Path, str]]]:
    association_table: dict[tuple[Path, str], list[tuple[Path, str]]] = {}

    # Itterate through all potential annotation files
    for annotation_file in root.rglob("*.geojson"):
        re_match: re.Match[str] | None = ANNOTATION_FILE_REGEX.match(annotation_file.name)

        # Continue if invalid file
        if not annotation_file.is_file() or not re_match:
            continue

        match_fields = re_match.groupdict()

        image_name: str = match_fields["image_name"]

        mask_files: list[tuple[Path, str]] = find_associated_mask_files(root, image_name)

        association_table[(annotation_file, image_name)] = mask_files

    return association_table
