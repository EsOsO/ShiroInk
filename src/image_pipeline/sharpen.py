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


# Legacy function for backward compatibility
def sharpen(img: Image.Image, factor: float = 1.2) -> Image.Image:
    """
    Sharpen the image to improve the quality for Kindle devices.
    
    This is a legacy function maintained for backward compatibility.
    Consider using SharpenStep instead.
    """
    step = SharpenStep(factor=factor)
    return step.process(img)
