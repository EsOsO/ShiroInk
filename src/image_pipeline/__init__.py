from .contrast import contrast
from .resize import resize
from .sharpen import sharpen
from .quantize import quantize
from .save import save
from PIL import Image


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
        image = contrast(image)
        resized_images = resize(image, resolution, rtl)

        for i, img in enumerate(resized_images):
            img = sharpen(img)
            img = quantize(img)

            # Save the image
            if len(resized_images) > 1:
                page_suffix = f"_page_{i+1}"
                output_path_with_suffix = output_path.with_stem(
                    output_path.stem + page_suffix
                )
                save(img, output_path_with_suffix, quality)
            else:
                save(img, output_path, quality)


__all__ = ["process"]
