from PIL import Image

from functions.get_ext import get_ext_from_file
from models.task import CompressTask


def compress_image(image, compress_task: CompressTask, overwrite):
    img = Image.open(image)
    image_ext = get_ext_from_file(image)
    new_image_name = image.replace(image_ext, f'_new{image_ext}')

    if overwrite:
        if image_ext == '.jpg' or image_ext == '.jpeg':
            img.save(image, 'JPEG', quality=compress_task.quality)
        else:
            img.save(image, optimize=True, quality=compress_task.quality)
        return image

    if image_ext == '.jpg' or image_ext == '.jpeg':
        img.save(new_image_name, 'JPEG', quality=compress_task.quality)
    else:
        img.save(new_image_name, optimize=True, quality=compress_task.quality)
    return new_image_name
