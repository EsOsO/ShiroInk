from PIL import Image


def quantize(img: Image):
    """
    Quantize the image to 16 colors.
    Args:
        img: The image to be quantized.
    Returns:
        The quantized image.
    """
    Palette16 = [
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

    colors = len(Palette16) // 3
    if colors < 256:
        Palette16 += Palette16[:3] * (256 - colors)
    palImg = Image.new("P", (1, 1))
    palImg.putpalette(Palette16)
    img = img.convert("L")
    img = img.convert("RGB")
    img = img.quantize(palette=palImg)
    img = img.convert("P")
    return img
