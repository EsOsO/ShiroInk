from PIL import Image, ImageOps


def resize(
    image: Image.Image, resolution: tuple[int, int], rtl: bool = False
) -> list[Image.Image]:
    """
    Resize the image to the given resolution. If the image is detected as a 2-page manga,
    split it into two single-page images and resize both.

    Args:
        image: The image to be resized.
        resolution: The target resolution as a tuple (width, height).
        rtl: Flag to switch the order of two-page images.

    Returns:
        A list of resized images.
    """
    width, height = image.size

    # Detect if the image is a 2-page manga
    if width > height:
        # Split the image into two single-page images
        left_page = image.crop((0, 0, width // 2, height))
        right_page = image.crop((width // 2, 0, width, height))

        # Resize both images
        left_page_resized = ImageOps.pad(
            left_page, resolution, method=Image.Resampling.LANCZOS, color="white"
        )
        right_page_resized = ImageOps.pad(
            right_page, resolution, method=Image.Resampling.LANCZOS, color="white"
        )

        if rtl:
            return [right_page_resized, left_page_resized]
        else:
            return [left_page_resized, right_page_resized]
    else:
        # Resize the single-page image
        img_resized = ImageOps.pad(
            image, resolution, method=Image.Resampling.LANCZOS, color="white"
        )
        return [img_resized]
