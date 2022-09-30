from PIL import Image

from functions.get_ext import get_ext_from_file
from models.task import TaskCompress


def compress_image(image, compress_task: TaskCompress, overwrite):
    img = Image.open(image)
    image_ext = get_ext_from_file(image)
    new_image_name = image.replace(image_ext, f'_new{image_ext}')

    if overwrite:
        img.save(image, optimize=True, quality=compress_task.quality)
        return image

    img.save(new_image_name, optimize=True, quality=compress_task.quality)
    return new_image_name
