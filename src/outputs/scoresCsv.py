#!/usr/bin/env python3

import csv

from pathlib import Path

import src.datatypes as dt

class ScoresCsv():
    def run(self, data: dt.Sample, output_directory: Path) -> None:
        """
        Outputs the results of one dataset to a csv file.

        Parameters:
            data: Dataset to save the results of.
        """
        output_directory.mkdir(parents=True, exist_ok=True)


        output_file = output_directory / "accuracy_scores.csv"
        output_row = {
            "Image Name": data.metadata.image_name,
            "Points File": data.metadata.points_file,
            "Mask File": data.metadata.mask_file,
            "Model Name": data.metadata.model_name,
            "False Negatives": data.results.falseNegative,
            "True Positives": data.results.truePositive,
            "False Positives": data.results.falsePositive,
            "Precision": data.results.precision,
            "Recall": data.results.recall,
            "F1": data.results.f1
        }
        #print(f"Precision: {data.results.precision}")
        #print(f"Recall: {data.results.recall}")
        #print(f"F1: {data.results.f1}")


        file_exists: bool = Path(output_file).exists()

        with open(output_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=output_row.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(output_row)

        pass
