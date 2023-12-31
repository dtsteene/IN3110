"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import io
from . import timing


def scale_image(scale: int, file: str) -> Image:
    im = Image.open(file)
    resized = im.resize((im.width // scale, im.height // scale))
    return np.asarray(resized)


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Runns the selected filter
    interpreting scale argument as new size = 1:scale of original
    """
    image = io.read_image(file)

    if scale != 1:
        image = scale_image(scale, file)

    filter = instapy.get_filter(filter, implementation)
    filtered = filter(image)

    if out_file:
        io.write_image(filtered, out_file)
    else:
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Displays or saves image with chosen filter and implementation")

    parser.add_argument("file",
                        help="The filename of the image to apply filter to")

    parser.add_argument("-o", "--out", required=False, default=None,
                        help="The output filename")

    parser.add_argument("-i", "--implementation", default='python', choices={'python', 'numpy', 'numba'}, required=False,
                        help="The implementation")

    # Refer to added argument in order to throw error if invalid
    scale_parse = parser.add_argument(
        "-sc", "--scale", required=False, default=1, help="Scale factor to resize image", type=int)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-g", "--gray", action='store_true', required=False,
                       help="Select gray filter")

    group.add_argument("-se", "--sepia", action='store_true',
                       help="Select sepia filter")

    parser.add_argument("-r", "--runtime", action='store_true', required=False,
                        help="average runtime of 3 runs for chosen implementation and file")

    args = parser.parse_args()

    # Check for invalid scale
    if args.scale == 0:
        raise argparse.ArgumentError(scale_parse, "Scale cannot be 0.")

    if args.sepia:
        filt = "color2sepia"
    else:
        filt = "color2gray"

    if args.runtime:
        filter_func = instapy.get_filter(filt, args.implementation)
        im_arr = io.read_image(args.file)

        if args.scale != 1:
            im_arr = scale_image(args.scale ,args.file)

        runtime = timing.time_one(filter_func, im_arr)
        print(f"Average time over 3 runs: {runtime}s")

    run_filter(
        file=args.file,
        out_file=args.out,
        implementation=args.implementation,
        filter=filt,
        scale=args.scale,
    )
