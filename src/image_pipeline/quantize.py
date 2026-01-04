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


def create_palette_from_bit_depth(bit_depth: int, color_mode: bool = False) -> bytes | None:
    """
    Create an optimized palette based on device bit depth.
    
    Args:
        bit_depth: Target bit depth (4=16 colors, 8=256 colors, etc.)
        color_mode: True for color palette, False for grayscale
    
    Returns:
        Palette as bytes, or None to use automatic quantization
    """
    num_colors = min(2 ** bit_depth, 256)  # Cap at 256 for PIL
    
    if not color_mode:
        # Grayscale palette - evenly distributed levels
        palette = []
        for i in range(num_colors):
            # Perceptually distributed grayscale
            val = int((i / (num_colors - 1)) * 255) if num_colors > 1 else 0
            palette.extend([val, val, val])
        
        # Pad to 256 colors if needed
        while len(palette) < 768:  # 256 * 3
            palette.extend(palette[:3])
        
        return bytes(palette[:768])
    else:
        # Color palette - use PIL's automatic quantization
        # (More sophisticated than simple color space division)
        return None


class QuantizeStep(ProcessingStep):
    """Processing step to quantize images to a limited color palette."""

    def __init__(
        self, 
        palette: bytes | None = Palette16,
        colors: int | None = None,
        use_bit_depth: bool = False,
        bit_depth: int = 4,
        color_mode: bool = False
    ):
        """
        Initialize the quantization step.

        Args:
            palette: Color palette to quantize to (default: 16 grayscale colors).
                     If None, uses automatic quantization.
            colors: Number of colors to quantize to (overrides palette).
            use_bit_depth: If True, creates palette from bit_depth parameter.
            bit_depth: Target bit depth for palette creation (4=16, 8=256, etc.).
            color_mode: True for color palette, False for grayscale.
        """
        super().__init__(
            palette=palette,
            colors=colors,
            use_bit_depth=use_bit_depth,
            bit_depth=bit_depth,
            color_mode=color_mode
        )
        
        # Determine final palette and color count
        if use_bit_depth:
            # Create palette from bit depth
            self.palette = create_palette_from_bit_depth(bit_depth, color_mode)
            self.colors = min(2 ** bit_depth, 256)
        elif colors is not None:
            # Use specified color count with automatic palette
            self.palette = None
            self.colors = min(colors, 256)
        elif palette is not None:
            # Use provided palette
            self.palette = palette
            self.colors = len(palette) // 3
        else:
            # Default: 16 grayscale colors
            self.palette = Palette16
            self.colors = 16

    def process(self, image: Image.Image) -> Image.Image:
        """
        Quantize the image to the specified palette.

        Args:
            image: Input PIL Image.

        Returns:
            Quantized image.
        """
        if self.palette is not None:
            # Use custom palette
            colors = min(self.colors, 256)
            palette = self.palette
            
            # Pad palette to 256 colors if needed
            if colors < 256:
                palette = palette + palette[:3] * (256 - colors)
            
            palette_img = Image.new("P", (1, 1))
            palette_img.putpalette(palette)

            return image.quantize(colors=colors, palette=palette_img)
        else:
            # Use automatic quantization with specified color count
            return image.quantize(colors=self.colors)

    def get_name(self) -> str:
        """Get the name of this step."""
        return f"Quantize({self.colors})"


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

