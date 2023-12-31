from instapy.python_filters import python_color2gray, python_color2sepia
import numpy as np
import numpy.testing as nt
from PIL import Image
import random
from conftest import *


def index_4_random_pixel(image):
    rand_i1 = random.randint(0, np.shape(image)[0]-1)
    rand_i2 = random.randint(0, np.shape(image)[1]-1)
    rand_i3 = random.randint(0, np.shape(image)[2]-1)
    return rand_i1, rand_i2, rand_i3


def test_color2gray(image):
    gray_image = python_color2gray(image)
    assert np.shape(image) == np.shape(gray_image)
    assert isinstance(gray_image, np.ndarray)
    assert (gray_image[:, :, 0] == gray_image[:, :, 1]).all() and (
        gray_image[:, :, 2] == gray_image[:, :, 1]).all()

    def check_random_pixel():
        rand_i = index_4_random_pixel(image)
        manual_graying = np.sum(
            image[rand_i[0], rand_i[1]] * np.array([0.21,  0.72, 0.07]))
        manual_graying = manual_graying.astype("uint8")
        nt.assert_allclose(gray_image[rand_i],
                           manual_graying, rtol=1e-05, atol=1e-05)
    check_random_pixel()
    check_random_pixel()
    check_random_pixel()


def test_color2sepia(image):
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ])
    sepia_image = python_color2sepia(image)

    def check_random_pixel():
        rand_i = index_4_random_pixel(image)
        manual_sepia = sepia_matrix @ image[rand_i[0], rand_i[1]]
        manual_sepia = np.minimum(manual_sepia, 255)
        manual_sepia = manual_sepia.astype("uint8")
        nt.assert_allclose(
            sepia_image[rand_i[0], rand_i[1]],  manual_sepia, rtol=1e-04, atol=1e-04)
    check_random_pixel()
    check_random_pixel()
    check_random_pixel()
    assert np.shape(image) == np.shape(sepia_image)
    assert isinstance(sepia_image, np.ndarray)
