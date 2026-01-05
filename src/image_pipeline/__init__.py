from pathlib import Path
from .contrast import ContrastStep
from .resize import resize
from .resize_step import ResizeStep
from .sharpen import SharpenStep
from .quantize import QuantizeStep, create_palette_from_bit_depth
from .color_profile import ColorProfileStep
from .crop import SmartCropStep
from .rotation import AutoRotateStep
from .text_enhance import TextEnhanceStep, AdaptiveTextEnhanceStep
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
    Process the image by applying pipeline steps and saving it.

    Processing order (CRITICAL for maintaining exact device resolution):
    1. Apply pipeline steps that should happen BEFORE resize
       (crop, rotate, enhance)
    2. Resize to exact device resolution (via ResizeStep in pipeline)
    3. Apply pipeline steps that should happen AFTER resize
       (contrast, sharpen, quantize)
    4. Save the image

    This ensures the final image is EXACTLY the device resolution, even after
    cropping blank areas.

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

    # Insert ResizeStep into pipeline at the correct position
    # (after pre-resize steps, before post-resize steps)
    pipeline_with_resize = _insert_resize_step(pipeline, resolution)

    # Open the image
    with Image.open(image_path).convert("RGB") as image:
        # Check if this is a double-page spread that needs splitting
        width, height = image.size
        if width > height:
            # Split into two pages and process each
            left_page = image.crop((0, 0, width // 2, height))
            right_page = image.crop((width // 2, 0, width, height))

            pages = [right_page, left_page] if rtl else [left_page, right_page]

            for i, page in enumerate(pages):
                # Process through the complete pipeline (includes ResizeStep)
                processed_img = pipeline_with_resize.process(page)

                # Save with page suffix
                page_suffix = f"_page_{i+1}"
                output_path_with_suffix = output_path.with_stem(
                    output_path.stem + page_suffix
                )
                save(processed_img, output_path_with_suffix, quality)
        else:
            # Single page - process through pipeline
            processed_img = pipeline_with_resize.process(image)
            save(processed_img, output_path, quality)


def _insert_resize_step(
    pipeline: ImagePipeline, resolution: tuple[int, int]
) -> ImagePipeline:
    """
    Insert a ResizeStep into the pipeline at the correct position.

    The ResizeStep should be placed:
    - AFTER: Crop, Rotate, TextEnhance steps
    - BEFORE: ColorProfile, Contrast, Sharpen, Quantize steps

    Args:
        pipeline: The original pipeline.
        resolution: Target resolution for the ResizeStep.

    Returns:
        New pipeline with ResizeStep inserted at the correct position.
    """
    # Create new pipeline with steps in correct order
    new_pipeline = ImagePipeline()
    resize_inserted = False

    for step in pipeline.steps:
        step_name = step.get_name()

        # Insert ResizeStep before post-resize steps
        if not resize_inserted and not any(
            keyword in step_name
            for keyword in ["Crop", "Rotate", "TextEnhance", "Resize"]
        ):
            new_pipeline.add_step(ResizeStep(resolution=resolution))
            resize_inserted = True

        # Don't add existing ResizeStep (we'll add our own)
        if "Resize" not in step_name:
            new_pipeline.add_step(step)

    # If resize wasn't inserted yet (all steps were pre-resize), add it at the end
    if not resize_inserted:
        new_pipeline.add_step(ResizeStep(resolution=resolution))

    return new_pipeline


__all__ = [
    "process",
    "ProcessingStep",
    "ImagePipeline",
    "PipelinePresets",
    "ContrastStep",
    "SharpenStep",
    "QuantizeStep",
    "ColorProfileStep",
    "SmartCropStep",
    "AutoRotateStep",
    "TextEnhanceStep",
    "AdaptiveTextEnhanceStep",
    "ResizeStep",
    "DeviceSpecs",
    "DeviceSpec",
    "DisplayType",
    "ColorGamut",
    "create_palette_from_bit_depth",
    # Utility functions (still needed)
    "resize",
    "save",
]
