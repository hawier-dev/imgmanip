import os

from PIL import Image

from functions.get_ext import get_ext_from_file
from models.task import ConvertTask


def convert_image(image, convert_task: ConvertTask, overwrite):
    img = Image.open(image)
    new_image = image.replace(get_ext_from_file(image), convert_task.convert_ext.value)
    new_image_name = image.replace(get_ext_from_file(image), '_new' + str(convert_task.convert_ext.value))

    # Overwrite old files
    if overwrite:
        img.save(new_image)
        os.remove(image)
        return new_image

    img.save(new_image_name)
    return new_image_name
