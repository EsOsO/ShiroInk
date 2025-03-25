from PIL import Image, ImageFilter, ImageOps
import numpy as np


def sharpen(img: Image) -> Image:
    """
    Sharpen the image to improve the quality for Kindle devices."
    """

    img.convert("L")
    unsharpFilter = ImageFilter.UnsharpMask(radius=1, percent=100)
    img = img.filter(unsharpFilter)
    img = img.filter(ImageFilter.BoxBlur(0.5))
    img = img.filter(unsharpFilter)
    return img
