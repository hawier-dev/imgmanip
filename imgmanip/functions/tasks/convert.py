import os
from os.path import basename

from PIL import Image

from functions.get_ext import get_ext_from_file
from models.save_type import SaveType
from models.task import ConvertTask


def convert_image(image, convert_task: ConvertTask, save_type: SaveType, out_path=None):
    img = Image.open(image)

    if save_type == SaveType.SELECT_PATH:
        new_file_name = out_path + '/' + basename(image).replace(get_ext_from_file(image),
                                                                 str(convert_task.convert_ext.value))
    elif save_type == SaveType.IMAGE_PATH:
        new_file_name = image.replace(get_ext_from_file(image), '_new' + str(convert_task.convert_ext.value))
    else:
        os.remove(image)
        new_file_name = image.replace(get_ext_from_file(image), str(convert_task.convert_ext.value))

    img.save(new_file_name)
    return new_file_name
