from PIL import Image, ImageOps

from imgmanip.functions.save_img import save_image_path
from imgmanip.models.axis import Axis
from imgmanip.models.save_type import SaveType
from imgmanip.models.task import FlipTask


def flip_image(image, flip_task: FlipTask, save_type: SaveType, out_path=None):
    img = Image.open(image)
    if flip_task.axis == Axis.HORIZONTAL:
        img = ImageOps.mirror(img)
    elif flip_task.axis == Axis.VERTICAL:
        img = ImageOps.flip(img)

    new_file_name = save_image_path(image_path=image, save_type=save_type, out_path=out_path)

    img.save(new_file_name)
    return new_file_name
