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
    logger.info("Converting pillow image to 2d matrix")
    width, height = image.size

    pixel_matrix = []

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


def show_image(image: Image) -> None:
    """
    Shows an image
    """
    logger.info("Showing image")
    plt.imshow(image, cmap="gray")


def plot_images_with_histograms(old_image: list[list[int]], new_image: list[list[int]], method: str):
    from .services import calculate_cumulative_histogram, calculate_image_histogram

    old_histogram = calculate_image_histogram(old_image)
    old_cumulative_histogram = calculate_cumulative_histogram(old_histogram)

    new_histogram = calculate_image_histogram(new_image)
    new_cumulative_histogram = calculate_cumulative_histogram(new_histogram)

    # 3 images, 2 rows
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    fig.suptitle(f"{method} Processing")
    axs[0, 0].imshow(old_image, cmap="gray")
    axs[0, 0].set_title("Original Image")
    axs[0, 1].plot(old_histogram)
    axs[0, 1].set_title("Original Histogram")
    axs[1, 0].imshow(new_image, cmap="gray")
    axs[1, 0].set_title("Processed Image")
    axs[1, 1].plot(new_histogram)
    axs[1, 1].set_title("Processed Histogram")
    axs[2, 0].plot(old_cumulative_histogram)
    axs[2, 0].set_title("Original Cumulative Histogram")
    axs[2, 1].plot(new_cumulative_histogram)
    axs[2, 1].set_title("Processed Cumulative Histogram")
    plt.show()
    plt.savefig(f"{ASSETS_PATH}{method}_processing.png")
