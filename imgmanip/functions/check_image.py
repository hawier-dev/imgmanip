image_extensions = [".jpg", ".jpeg", ".tif", ".bmp", ".png", ".gif"]


def check_image_file(image):
    for image_ext in image_extensions:
        if image.endswith(image_ext):
            return True
    return False
