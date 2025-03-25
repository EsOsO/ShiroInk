from PIL import Image, ImageOps


def contrast(img: Image, gamma: float = 0.8):
    return ImageOps.autocontrast(
        Image.eval(img, lambda a: int(255 * (a / 255.0) ** gamma))
    )
