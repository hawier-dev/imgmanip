import cv2
from PIL import Image, ImageOps

from functions.get_ext import get_ext_from_file
from models.axis import Axis
from models.task import FlipTask


def flip_image(image, flip_task: FlipTask, overwrite):
    img = Image.open(image)
    if flip_task.axis == Axis.HORIZONTAL:
        img = ImageOps.mirror(img)
    elif flip_task.axis == Axis.VERTICAL:
        img = ImageOps.flip(img)
    image_ext = get_ext_from_file(image)
    new_image_name = image.replace(image_ext, f'_new{image_ext}')

    if overwrite:
        img.save(image)
        return image

    img.save(new_image_name)
    return new_image_name
