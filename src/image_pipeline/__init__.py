from pathlib import Path
from .contrast import contrast, ContrastStep
from .resize import resize
from .sharpen import sharpen, SharpenStep
from .quantize import quantize, QuantizeStep, create_palette_from_bit_depth
from .color_profile import ColorProfileStep
from .save import save
from .pipeline import ProcessingStep, ImagePipeline
from .presets import PipelinePresets
from .devices import DeviceSpecs, DeviceSpec, DisplayType, ColorGamut
from PIL import Image


def process(
    image_path: Path,
    output_path: Path,
    resolution: tuple[int, int],
    rtl: bool = False,
    quality: int = 85,
    pipeline: ImagePipeline | None = None,
) -> None:
    """
    Process the image by resizing, applying pipeline steps, and saving it.

    Args:
        image_path: The path to the image to be processed.
        output_path: The path to save the processed image.
        resolution: The target resolution as a tuple (width, height).
        rtl: Flag to switch the order of two-page images.
        quality: The quality level for optimization (1-100).
        pipeline: Custom ImagePipeline to use. If None, uses default Kindle pipeline.
    """
    # Use default Kindle pipeline if none provided
    if pipeline is None:
        pipeline = PipelinePresets.kindle()

    # Open the image
    with Image.open(image_path).convert("RGB") as image:
        resized_images = resize(image, resolution, rtl)

        for i, img in enumerate(resized_images):
            # Process through the pipeline
            processed_img = pipeline.process(img)

            # Save the image
            if len(resized_images) > 1:
                page_suffix = f"_page_{i+1}"
                output_path_with_suffix = output_path.with_stem(
                    output_path.stem + page_suffix
                )
                save(processed_img, output_path_with_suffix, quality)
            else:
                save(processed_img, output_path, quality)


__all__ = [
    "process",
    "ProcessingStep",
    "ImagePipeline",
    "PipelinePresets",
    "ContrastStep",
    "SharpenStep",
    "QuantizeStep",
    "ColorProfileStep",
    "DeviceSpecs",
    "DeviceSpec",
    "DisplayType",
    "ColorGamut",
    # Legacy functions
    "contrast",
    "sharpen",
    "quantize",
    "resize",
    "save",
]
