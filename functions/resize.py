from PIL import Image

from functions.get_ext import get_ext_from_file
from models.task import ResizeTask


# TODO: KILKA RAZY WIEKSZE ZDJECIE ITD
def resize_image(image, resize_task: ResizeTask, overwrite):
    # Image
    img = Image.open(image)
    width, height = img.size
    image_ext = get_ext_from_file(image)
    new_image_name = image.replace(image_ext, f'_new{image_ext}')

    img = img.resize((int(resize_task.new_width), int(resize_task.new_height)))
    if overwrite:
        img.save(image)
        return image

    img.save(new_image_name)
    return new_image_name
