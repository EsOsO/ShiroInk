from PIL import Image, ImageEnhance
from .pipeline import ProcessingStep


class SharpenStep(ProcessingStep):
    """Processing step to sharpen images."""

    def __init__(self, factor: float = 1.2):
        """
        Initialize the sharpening step.

        Args:
            factor: Sharpness enhancement factor (1.0 = no change, >1.0 = sharper).
        """
        super().__init__(factor=factor)
        self.factor = factor

    def process(self, image: Image.Image) -> Image.Image:
        """
        Apply sharpening to the image.

        Args:
            image: Input PIL Image.

        Returns:
            Sharpened image.
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(self.factor)

    def get_name(self) -> str:
        """Get the name of this step."""
        return "Sharpen"
