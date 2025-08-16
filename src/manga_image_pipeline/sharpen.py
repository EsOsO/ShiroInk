from PIL import Image, ImageFilter


def sharpen_image(image: Image) -> Image:
    """Apply a sharpening filter to the image"""

    sharpened_image = image.filter(ImageFilter.SHARPEN)
    return sharpened_image


def apply_grey_palette(image: Image, palette) -> Image:
    colors = len(palette) // 3
    if colors < 256:
        palette = palette + palette[:3] * (256 - colors)

    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(palette)

    return image.quantize(palette=pal_img)
