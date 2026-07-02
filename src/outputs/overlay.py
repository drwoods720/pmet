#!/usr/bin/env python3
"""
overlay.py

Defines the :class:`Overlay` output generator, which produces
a colour-coded overlay image visualizing per-cell accuracy against
the original segmentation mask.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import numpy.typing as npt

from pathlib import Path
from PIL import Image

import src.datatypes as dt

from src.outputs.output import Output


class Overlay(Output):
    """
    Generate a colour-coded overlay image for a sample.

    Produces an image based on the original segmentation mask, where
    each cell is color coded according to its classification
    accuracy.
    """

    def overlay_image(
        self,
        background: npt.NDArray[np.uint16],
        overlay: npt.NDArray[np.uint16],
        alpha: float = 1.0,
    ) -> npt.NDArray[np.uint16]:
        """
        Overlay one image on top of another with optional transparency.

        :param background: The background image.
        :type background: npt.NDArray[np.uint16]

        :param overlay: The image to overlay on top of the background image.
        :type background: npt.NDArray[np.uint16]

        :param alpha: The transparency value of the overlay image, in the
            range ``0`` (fully transparent) to ``1`` (fully opaque).
        :type alpha: float

        :returns: The background image with the overlay image blended on
            top of it.
        :rtype: npt.NDArray[np.uint16]
        """
        bg: Image.Image = Image.fromarray(background).convert("RGB")
        ov: Image.Image = Image.fromarray(overlay).convert("RGBA")

        ov_array = np.array(ov)
        is_background = np.all(ov_array[..., :3] == 0, axis=-1)
        ov_array[..., 3] = np.where(is_background, 0, int(255 * alpha))
        ov = Image.fromarray(ov_array)

        result = bg.copy()
        result.paste(ov, None, ov)

        return np.array(result.convert("RGB"))

    def generate_accuracy_mask(
        self, cells: dict[int, dt.Cell], mask: npt.NDArray[np.uint16]
    ) -> npt.NDArray[np.uint8]:
        """
        Create an accuracy-coded image from the segmentation mask.

        Builds an image based on the original segmentation mask,
        colour coded per cell according to its classification
        accuracy.

        :param cells: The list of cells to colour code in the image.
        :type cells: dict[int, ~.datatypes.Cell]

        :param mask: The original segmentation mask.
        :type mask: npt.NDArray[np.uint16]

        :returns: The original segmentation mask.
        :rtype: npt.NDArray[np.uint8]
        """
        accuracy_mask: npt.NDArray[np.uint8] = np.zeros_like(mask, dtype=np.uint8)

        true_positives: list[int] = []
        false_positives: list[int] = []
        oversegmented: list[int] = []
        clipping: list[int] = []

        for cell in cells.values():
            if cell.clipping:
                clipping.append(cell.id)
            elif len(cell.points) == 0:
                false_positives.append(cell.id)
            elif len(cell.points) > 1:
                oversegmented.append(cell.id)
            else:
                true_positives.append(cell.id)

        accuracy_mask[np.isin(mask, true_positives)] = 1
        accuracy_mask[np.isin(mask, false_positives)] = 2
        accuracy_mask[np.isin(mask, oversegmented)] = 3
        accuracy_mask[np.isin(mask, clipping)] = 4

        return accuracy_mask

    def run(self, data: dt.Sample, output_directory: Path) -> None:
        """
        Generate and write the accuracy overlay image for a sample.

        Builds the accuracy-coded image via :meth:`generate_accuracy_mask`,
        optionally blends it over the sample's original image via
        :func:`overlay_image`, and writes the result to
        ``output_directory``.

        :param data: The processed sample data to generate the
            overlay image from.
        :type data: ~.datatypes.Sample

        :param output_directory: The directory to write the
            generated overlay image to.
        :type output_directory: pathlib.Path

        :returns: None. The generated image will be written as a side
            effect to a file within ``output_directory``.
        :rtype: None
        """

        # Define graph and its limits
        fig, ax = plt.subplots()

        padding = 50  # Pixels

        # Crop into the points
        ax.set_ylim(data.sample_area.ymax + padding, data.sample_area.ymin - padding)
        ax.set_xlim(data.sample_area.xmin - padding, data.sample_area.xmax + padding)

        accuracy_mask: npt.NDArray[np.uint8] = self.generate_accuracy_mask(
            data.cells, data.mask
        )

        # Image compositing pipeline
        colors: npt.NDArray[np.uint8] = np.array(
            [
                [0, 0, 0],  # Background (black)
                [0, 255, 0],  # True positive (green)
                [255, 0, 0],  # False positive (red)
                [0, 0, 255],  # Oversegmented (blue)
                [128, 128, 128],  # Clipping (grey)
            ],
            dtype=np.uint8,
        )

        rgb_accuracy_mask: npt.NDArray[np.uint8] = colors[accuracy_mask]

        # Overlay image
        overlaid_image = self.overlay_image(data.original_image, rgb_accuracy_mask, 0.2)

        ax.imshow(overlaid_image, origin="upper", interpolation="none")

        for point in data.points:
            if point.cell == 0:
                color = "red"
            elif data.cells[point.cell].clipping:
                color = "gray"
            else:
                neighbours: int = len(data.cells[point.cell].points)
                if neighbours == 1:
                    color = "green"
                else:
                    color = "blue"

            ax.scatter(point.x, point.y, color=color, s=0.75)

        # Plot the sample area
        blx: int = data.sample_area.xmin
        bly: int = data.sample_area.ymin
        width: int = data.sample_area.xmax - blx
        height: int = data.sample_area.ymax - bly

        sample_border = patches.Rectangle(
            (blx, bly), width, height, edgecolor="r", facecolor="none", linewidth=0.2
        )
        ax.add_patch(sample_border)

        output_directory.mkdir(parents=True, exist_ok=True)

        output_file = (
            output_directory
            / f"{data.metadata.image_name}-{data.metadata.model_name}_accuracy_mask.png"
        )
        fig.savefig(fname=output_file, bbox_inches="tight", pad_inches=0, dpi=400)

        plt.close("all")
