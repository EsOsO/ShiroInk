from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image_pipeline.pipeline import ImagePipeline
    from error_handler import ErrorTracker


@dataclass
class ProcessingConfig:
    """Configuration for image processing operations."""

    src_dir: Path
    dest_dir: Path
    resolution: tuple[int, int] = (1404, 1872)
    rtl: bool = False
    quality: int = 6
    debug: bool = False
    dry_run: bool = False
    workers: int = 4
    pipeline_preset: str = "kindle"  # Name of the preset pipeline to use
    custom_pipeline: "ImagePipeline | None" = field(default=None, repr=False)
    continue_on_error: bool = True  # Continue processing even if some files fail
    max_retries: int = 3  # Maximum retries for I/O operations

    def __post_init__(self):
        """Validate configuration parameters."""
        if self.quality < 1 or self.quality > 9:
            raise ValueError("Quality must be between 1 and 9")
        if self.workers < 1:
            raise ValueError("Workers must be at least 1")
        if self.resolution[0] <= 0 or self.resolution[1] <= 0:
            raise ValueError("Resolution values must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries must be non-negative")

    def get_pipeline(self) -> "ImagePipeline":
        """
        Get the image processing pipeline to use.

        Returns:
            ImagePipeline instance based on configuration.
        """
        # Import here to avoid circular dependency
        from image_pipeline.presets import PipelinePresets

        if self.custom_pipeline is not None:
            return self.custom_pipeline
        else:
            return PipelinePresets.get_preset(self.pipeline_preset)
