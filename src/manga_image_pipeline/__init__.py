from .resize import resize_image
from .sharpen import sharpen_image, apply_grey_palette
from .save import save_image
from PIL import Image

Palette16 = [
    0x00,
    0x00,
    0x00,
    0x11,
    0x11,
    0x11,
    0x22,
    0x22,
    0x22,
    0x33,
    0x33,
    0x33,
    0x44,
    0x44,
    0x44,
    0x55,
    0x55,
    0x55,
    0x66,
    0x66,
    0x66,
    0x77,
    0x77,
    0x77,
    0x88,
    0x88,
    0x88,
    0x99,
    0x99,
    0x99,
    0xAA,
    0xAA,
    0xAA,
    0xBB,
    0xBB,
    0xBB,
    0xCC,
    0xCC,
    0xCC,
    0xDD,
    0xDD,
    0xDD,
    0xEE,
    0xEE,
    0xEE,
    0xFF,
    0xFF,
    0xFF,
]


def process(
    image_path: str,
    output_path: str,
    resolution: tuple[int, int],
    rtl: bool = False,
    quality: int = 85,
) -> None:
    """
    Process the image by resizing, sharpening, and saving it.

    Args:
        image_path: The path to the image to be processed.
        output_path: The path to save the processed image.
        resolution: The target resolution as a tuple (width, height).
        rtl: Flag to switch the order of two-page images.
        quality: The quality level for optimization (1-100).
    """
    # Open the image
    with Image.open(image_path) as image:
        # Resize the image
        resized_images = resize_image(image, resolution, rtl)

        for i, resized_image in enumerate(resized_images):
            # Sharpen the image
            img = sharpen_image(resized_image)
            img = apply_grey_palette(img, Palette16)
            # Save the image
            if len(resized_images) > 1:
                page_suffix = f"_page_{i+1}"
                output_path_with_suffix = output_path.with_stem(
                    output_path.stem + page_suffix
                )
                save_image(img, output_path_with_suffix, quality)
            else:
                save_image(img, output_path, quality)


__all__ = ["process"]
