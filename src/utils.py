from loguru import logger
import matplotlib.pyplot as plt

from PIL import Image
from src.constants import ASSETS_PATH, IMAGE_ORIGINAL_PATH, IMAGE_PROCESSED_PATH


def open_image_as_grayscale(path: str) -> Image:
    """
    Opens an image from a given path and converts it to grayscale
    """
    logger.info(f"Opening image from path: {path}")
    return Image.open(f"{IMAGE_ORIGINAL_PATH}{path}.jpg").convert("L")


def convert_pillow_image_to_2d_matrix(image: Image) -> list[list[int]]:
    # Get the dimensions of the image
    width, height = image.size

    # Create a 2D list to store the pixel values
    pixel_matrix = []

    # Iterate through the image and store pixel values in the 2D list
    for y in range(height):
        row = []
        for x in range(width):
            pixel_value = image.getpixel((x, y))
            row.append(pixel_value)
        pixel_matrix.append(row)

    return pixel_matrix


def convert_2d_matrix_to_pillow_image(matrix: list[list[int]], width: int, height: int) -> Image:
    """
    Converts a 2d matrix of pixels to a pillow image
    """
    return Image.new("L", (width, height)).putdata(matrix)


def write_pillow_image_to_file(image: Image, image_num: str, processing_name: str) -> None:
    """
    Writes a pillow image to a file
    """
    logger.info(f"Writing image to file: {IMAGE_PROCESSED_PATH}{image_num}_{processing_name}.jpg")
    image.save(f"{IMAGE_PROCESSED_PATH}{image_num}_{processing_name}.jpg")


def plot_histogram(histogram: list[int], label: str = "") -> None:
    """
    Plots a histogram
    """
    logger.info(f"Plotting histogram for image: {label}")
    plt.plot(histogram)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()
    plt.savefig(f"{ASSETS_PATH}{label}_histogram.png")
