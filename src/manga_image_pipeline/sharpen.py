from PIL import Image, ImageFilter


def sharpen_image(image: Image) -> Image:
    """Apply a sharpening filter to the image"""

    sharpened_image = image.filter(ImageFilter.SHARPEN)
    return sharpened_image


def apply_grey_palette(image: Image, palette) -> Image:
    return image.quantize(colors=16)
