"""numba-optimized filters"""
from numba import jit
import numpy as np


@jit(nopython=True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    def gray(rgb: np.array):
        """Calculates and assigns gray value of pixels given and returns a list
        of their respective gray values.

        Args:
            rgb (np.array)
        Returns:
            List: [gray, gray, gray]

        """
        # Weights for RGB respectively
        weights = (0.21, 0.72, 0.07)

        gray = weights[0] * rgb[0] + weights[1] * rgb[1] + weights[2] * rgb[2]
        return [gray, gray, gray]

    # For every pixel in the image, calculate and assign gray values
    gray_image = np.array([np.array([gray(rgb) for rgb in h]) for h in image])

    return gray_image.astype('uint8')


@jit(nopython=True)
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """

    sepia_image = np.empty_like(image)
    image_height = np.shape(sepia_image)[0]
    image_width = np.shape(sepia_image)[1]

    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]

    # Iterate over the pixels
    for i in range(image_height):
        for j in range(image_width):
            # Get values for each color respectively
            r, g, b = image[i, j, 0], image[i, j, 1], image[i, j, 2]

            # Apply the sepia matrix and cast to int
            r_new = int(
                sepia_matrix[0][0] * r + sepia_matrix[0][1] * g + sepia_matrix[0][2] * b)
            g_new = int(
                sepia_matrix[1][0] * r + sepia_matrix[1][1] * g + sepia_matrix[1][2] * b)
            b_new = int(
                sepia_matrix[2][0] * r + sepia_matrix[2][1] * g + sepia_matrix[2][2] * b)

            # Normalize values if needed
            if r_new > 255:
                r_new = 255
            if g_new > 255:
                g_new = 255
            if b_new > 255:
                b_new = 255

            # Assign values
            sepia_image[i, j] = r_new, g_new, b_new

    return sepia_image.astype('uint8')
