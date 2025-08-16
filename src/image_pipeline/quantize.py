from PIL import Image

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


def quantize(img: Image, palette: bytes = Palette16) -> Image:
    """
    Quantize the image to 16 colors.
    Args:
        img: The image to be quantized.
    Returns:
        The quantized image.
    """

    colors = len(palette) // 3
    if colors < 256:
        palette += palette[:3] * (256 - colors)
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette)

    img = img.quantize(colors=colors, palette=palette_img)
    return img
