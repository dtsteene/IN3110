"""numpy implementation of image filters"""

from typing import Optional
import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)

    # Weights for RGB respectively
    weights = (0.21, 0.72, 0.07)

    # For each channel, set pixel value as weighted sum
    gray_value = image[:, :, 0] * weights[0] + image[:,
                                                     :, 1] * weights[1] + image[:, :, 2] * weights[2]
    gray_image[:, :, 0] = gray_value
    gray_image[:, :, 1] = gray_value
    gray_image[:, :, 2] = gray_value

    return gray_image.astype("uint8")


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ])

    # Tune the sepia matrix by an amount k
    sepia_matrix_tuned = (sepia_matrix - np.identity(3))*k + np.identity(3)

    # Apply the sepia matrix by taking the dot product of the image with the
    # sepia matrix
    sepia_image = image @ sepia_matrix_tuned.transpose()
    sepia_image = np.minimum(sepia_image, 255)
    return sepia_image.astype("uint8")
