from PIL import Image, ImageEnhance


def sharpen(img: Image, factor: float = 1.2) -> Image:
    """
    Sharpen the image to improve the quality for Kindle devices."
    """

    # Apply sharpening filter
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)
