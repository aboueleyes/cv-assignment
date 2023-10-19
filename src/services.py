import itertools
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

    for i, j in itertools.product(range(height), range(width)):
        if i + 1 < height:
            co_occurrence_matrix[matrix[i][j]][matrix[i + 1][j]] += 1
        if i >= 1:
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
    for item in matrix:
        for j in range(len(item)):
            contrast += item[j]

    return contrast


def calculate_image_histogram(matrix: list[list[int]]) -> list[int]:
    """
    Calculates the histogram of a 2d matrix of pixels
    """
    logger.info("Calculating histogram")
    histogram = [0 for _ in range(COLOR_DEPTH)]
    for item in matrix:
        for j in range(len(item)):
            try:
                histogram[item[j]] += 1
            except IndexError:
                print(f"item[j] = {item[j]}")
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


def get_color_at_percentage(cumulative_histogram: list[int], percentage: int) -> tuple[int]:
    """Get the color at a given percentage of the cumulative histogram."""
    logger.info(f"Getting color at percentage: {percentage}")
    max_value = cumulative_histogram[-1]
    start = (percentage / 100) * max_value
    end = ((100 - percentage) / 100) * max_value
    x, y = 0, 0
    for i, e in enumerate(cumulative_histogram):
        if e >= start:
            x = i
            break
    for i, e in reversed(list(enumerate(cumulative_histogram))):
        if e <= end:
            y = i
            break
    return x, y


def contrast_stretch(matrix: list[list[int]], a: int, b: int, c: int, d: int) -> list[list[int]]:
    logger.info("Contrast stretching")
    new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i, row in enumerate(matrix):
        for j, pixel in enumerate(row):
            new_pixel = (pixel - c) * ((b - a) / (d - c)) + a
            new_pixel = max(0, min(new_pixel, COLOR_DEPTH - 1))
            new_matrix[i][j] = round(new_pixel)
    return new_matrix


def equalize_histogram(matrix: list[list[int]], min_value: int, max_value: int) -> list[list[int]]:
    def get_first_bigger_than(arr: list[int], val: int) -> int:
        for i in range(COLOR_DEPTH):
            if arr[i] >= val:
                return i
        return COLOR_DEPTH - 1

    logger.info("Equalizing histogram")
    new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    hist = calculate_image_histogram(matrix)
    cumulative = calculate_cumulative_histogram(hist)
    cdf = [0] * COLOR_DEPTH
    for i in range(COLOR_DEPTH):
        new_color = (i / COLOR_DEPTH) * (max_value - min_value) + min_value
        cdf[i] = cumulative[round(new_color)]
    for i, row in enumerate(matrix):
        for j, pixel in enumerate(row):
            old_cum = cumulative[pixel]
            new_val = get_first_bigger_than(cdf, old_cum)
            new_matrix[i][j] = new_val
    return new_matrix


def gray_scale_transformation(matrix: list[list[int]], x1: int, y1: int, x2: int, y2: int) -> list[list[int]]:
    slope1 = y1 / x1
    slope2 = (y2 - y1) / (x2 - x1)
    slope3 = (COLOR_DEPTH - 1 - y2) / (COLOR_DEPTH - 1 - x2)
    new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i, row in enumerate(matrix):
        for j, pixel in enumerate(row):
            old_val = pixel
            new_val = 0
            if old_val < x1:
                new_val = slope1 * old_val
            elif old_val < x2:
                new_val = slope2 * (old_val - x1) + y1
            else:
                new_val = slope3 * (old_val - x2) + y2
            new_matrix[i][j] = round(new_val)
    for row in new_matrix:
        for pixel in row:
            if pixel >= COLOR_DEPTH:
                logger.error(f"{pixel}=")
    return new_matrix
