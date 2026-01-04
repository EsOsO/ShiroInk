from PIL import Image, ImageEnhance
from .pipeline import ProcessingStep


class ContrastStep(ProcessingStep):
    """Processing step to adjust image contrast."""

    def __init__(self, factor: float = 1.5):
        """
        Initialize the contrast adjustment step.

        Args:
            factor: Contrast enhancement factor (1.0 = no change, >1.0 = more contrast).
        """
        super().__init__(factor=factor)
        self.factor = factor

    def process(self, image: Image.Image) -> Image.Image:
        """
        Apply contrast adjustment to the image.

        Args:
            image: Input PIL Image.

        Returns:
            Image with adjusted contrast.
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(self.factor)

    def get_name(self) -> str:
        """Get the name of this step."""
        return "Contrast"
