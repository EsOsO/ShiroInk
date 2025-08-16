from PIL import Image, ImageEnhance


def contrast(img: Image.Image, factor: float = 1.5) -> Image.Image:
    """
    Adjust the contrast of the image to improve the quality for Kindle devices.
    """

    # Apply gamma correction to adjust contrast
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)
