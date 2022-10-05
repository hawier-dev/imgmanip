from os.path import basename

from functions.get_ext import get_ext_from_file
from models.save_type import SaveType


def save_image_path(image_path, save_type: SaveType, out_path=None):
    image_ext = get_ext_from_file(image_path)
    if save_type == SaveType.SELECT_PATH:
        new_file_name = out_path + '/' + basename(image_path)
    elif save_type == SaveType.IMAGE_PATH:
        new_file_name = image_path.replace(image_ext, f'_new{image_ext}')
    else:
        new_file_name = image_path

    return new_file_name
