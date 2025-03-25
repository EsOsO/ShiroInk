from PIL import Image


def save(image: Image, path: str, quality=3) -> None:
    """
    Save the image for Kindle devices by reducing file size while maintaining quality.

    Args:
        image: The image to be saved.
        path: The path to save the image.
        quality (int): The quality level for optimization (1-9).
    """
    # Save the optimized image to the specified path
    image.save(path, compress_level=quality)
