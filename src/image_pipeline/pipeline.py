"""
Processing pipeline abstraction for configurable image processing.
"""

from abc import ABC, abstractmethod
from typing import List
from PIL import Image


class ProcessingStep(ABC):
    """Abstract base class for image processing steps."""

    def __init__(self, **kwargs):
        """
        Initialize the processing step with configuration parameters.

        Args:
            **kwargs: Configuration parameters specific to this step.
        """
        self.config = kwargs

    @abstractmethod
    def process(self, image: Image.Image) -> Image.Image:
        """
        Process the image.

        Args:
            image: The input PIL Image.

        Returns:
            The processed PIL Image.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this processing step.

        Returns:
            A descriptive name for this step.
        """
        pass

    def __repr__(self) -> str:
        """String representation of the processing step."""
        return f"{self.get_name()}({self.config})"


class ImagePipeline:
    """Configurable image processing pipeline."""

    def __init__(self, steps: List[ProcessingStep] | None = None):
        """
        Initialize the image pipeline.

        Args:
            steps: List of processing steps to apply in order.
        """
        self.steps: List[ProcessingStep] = steps if steps is not None else []

    def add_step(self, step: ProcessingStep) -> "ImagePipeline":
        """
        Add a processing step to the pipeline.

        Args:
            step: The processing step to add.

        Returns:
            Self for method chaining.
        """
        self.steps.append(step)
        return self

    def remove_step(self, step_name: str) -> "ImagePipeline":
        """
        Remove a processing step by name.

        Args:
            step_name: The name of the step to remove.

        Returns:
            Self for method chaining.
        """
        self.steps = [s for s in self.steps if s.get_name() != step_name]
        return self

    def clear(self) -> "ImagePipeline":
        """
        Clear all processing steps.

        Returns:
            Self for method chaining.
        """
        self.steps = []
        return self

    def process(self, image: Image.Image) -> Image.Image:
        """
        Process an image through all steps in the pipeline.

        Args:
            image: The input PIL Image.

        Returns:
            The processed PIL Image.
        """
        result = image
        for step in self.steps:
            result = step.process(result)
        return result

    def get_steps(self) -> List[str]:
        """
        Get the names of all steps in the pipeline.

        Returns:
            List of step names.
        """
        return [step.get_name() for step in self.steps]

    def __repr__(self) -> str:
        """String representation of the pipeline."""
        step_names = " -> ".join(self.get_steps()) if self.steps else "empty"
        return f"ImagePipeline({step_names})"

    def __len__(self) -> int:
        """Get the number of steps in the pipeline."""
        return len(self.steps)
