from os.path import basename

from PIL import Image

from functions.get_ext import get_ext_from_file
from functions.save_img import save_image_path
from models.save_type import SaveType
from models.task import CompressTask


def compress_image(image, compress_task: CompressTask, save_type: SaveType, out_path=None):
    img = Image.open(image)
    image_ext = get_ext_from_file(image)

    new_file_name = save_image_path(image_path=image, save_type=save_type, out_path=out_path)

    if image_ext == '.jpg' or image_ext == '.jpeg':
        img.save(new_file_name, 'JPEG', quality=compress_task.quality)
    else:
        img.save(new_file_name, optimize=True, quality=compress_task.quality)
    return new_file_name
