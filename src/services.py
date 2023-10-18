from src.constants import COLOR_DEPTH
from loguru import logger


def calculate_co_occurrence_matrix(matrix: list[int]) -> list[list[int]]:
    """Calculates the co-occurrence matrix of a 2d matrix of pixels
    using north-south orientation.

    Args:
        matrix (list[list[int]]): a 2d matrix of pixels (grayscale)

    Returns:
        list[list[int]]: the co-occurrence matrix
    """
    logger.info("Calculating co-occurrence matrix")
    co_occurrence_matrix = [[0 for _ in range(COLOR_DEPTH)] for _ in range(COLOR_DEPTH)]
    width, height = len(matrix[0]), len(matrix)

    for i in range(height):
        for j in range(width):
            if i + 1 < height:
                co_occurrence_matrix[matrix[i][j]][matrix[i + 1][j]] += 1
            if i - 1 >= 0:
                co_occurrence_matrix[matrix[i][j]][matrix[i - 1][j]] += 1

    return co_occurrence_matrix


def use_co_occurrence_matrix(func):
    def wrapper(matrix: list[list[int]]) -> int:
        co_occurrence_matrix = calculate_co_occurrence_matrix(matrix)
        return func(co_occurrence_matrix)

    return wrapper


@use_co_occurrence_matrix
def calculate_contrast(matrix: list[list[int]]) -> int:
    """
    Calculates the contrast of a 2d matrix of pixels
    """
    logger.info("Calculating contrast")
    contrast = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            contrast += matrix[i][j]

    return contrast


def calculate_image_histogram(matrix: list[list[int]]) -> list[int]:
    """
    Calculates the histogram of a 2d matrix of pixels
    """
    logger.info("Calculating histogram")
    histogram = [0 for _ in range(COLOR_DEPTH)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            histogram[matrix[i][j]] += 1
    return histogram


def calculate_cumulative_histogram(histogram: list[int]) -> list[int]:
    """
    Calculates the cumulative histogram of a 2d matrix of pixels
    """
    logger.info("Calculating cumulative histogram")
    cumulative_histogram = [0 for _ in range(COLOR_DEPTH)]
    cumulative_histogram[0] = histogram[0]
    for i in range(1, COLOR_DEPTH):
        cumulative_histogram[i] = cumulative_histogram[i - 1] + histogram[i]
    return cumulative_histogram