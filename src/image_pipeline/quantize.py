from PIL import Image
from .pipeline import ProcessingStep

Palette16 = bytes(
    [
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
)


class QuantizeStep(ProcessingStep):
    """Processing step to quantize images to a limited color palette."""

    def __init__(self, palette: bytes = Palette16):
        """
        Initialize the quantization step.

        Args:
            palette: Color palette to quantize to (default: 16 grayscale colors).
        """
        super().__init__(palette=palette)
        self.palette = palette

    def process(self, image: Image.Image) -> Image.Image:
        """
        Quantize the image to the specified palette.

        Args:
            image: Input PIL Image.

        Returns:
            Quantized image.
        """
        colors = len(self.palette) // 3
        palette = self.palette
        if colors < 256:
            palette = palette + palette[:3] * (256 - colors)
        palette_img = Image.new("P", (1, 1))
        palette_img.putpalette(palette)

        return image.quantize(colors=colors, palette=palette_img)

    def get_name(self) -> str:
        """Get the name of this step."""
        return "Quantize"


# Legacy function for backward compatibility
def quantize(img: Image.Image, palette: bytes = Palette16) -> Image.Image:
    """
    Quantize the image to 16 colors.

    This is a legacy function maintained for backward compatibility.
    Consider using QuantizeStep instead.

    Args:
        img: The image to be quantized.
        palette: Color palette to use.
    Returns:
        The quantized image.
    """
    step = QuantizeStep(palette=palette)
    return step.process(img)
