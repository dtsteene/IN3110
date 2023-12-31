"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
from instapy import io
from typing import Callable
import numpy as np


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    # return the _average_ time of one call
    times = []
    for _ in range(calls):
        start = time.perf_counter()
        filter_function(arguments[0])
        end = time.perf_counter()
        times.append(end-start)
    return sum(times)/len(times)


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    image = io.read_image(filename)
    print(
        f"Timing performed using {filename}: {np.shape(image)[0]}x{np.shape(image)[1]}")
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = instapy.get_filter(filter_name)
        # time the reference implementations
        pixels = io.read_image(filename)
        reference_time = time_one(reference_filter, pixels, calls)
        print()
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        implementations = ["numpy", "numba"]
        for implementation in implementations:
            filter = instapy.get_filter(filter_name, implementation)
            first_call = time_one(filter, pixels, 1)
            filter_time = time_one(filter, pixels, int(calls-1))
            speedup = reference_time/filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s first call: {first_call:.3}s (speedup w/o first call ={speedup:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
