from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
import numpy as np
import numpy.testing as nt
from PIL import Image
import instapy
from conftest import *


def test_color2gray(image, reference_gray):
    gray_image = numpy_color2gray(image)
    nt.assert_allclose(gray_image, reference_gray, rtol=1e-05, atol=1e-05)
    assert np.shape(image) == np.shape(gray_image)
    assert isinstance(gray_image, np.ndarray)
    assert (gray_image[:, :, 0] == gray_image[:, :, 1]).all() and (
        gray_image[:, :, 2] == gray_image[:, :, 1]).all()


def test_color2sepia(image, reference_sepia):
    sepia_image = numpy_color2sepia(image)
    nt.assert_allclose(sepia_image, reference_sepia, rtol=1e-04, atol=1)
    assert np.shape(image) == np.shape(sepia_image)
    assert isinstance(sepia_image, np.ndarray)
