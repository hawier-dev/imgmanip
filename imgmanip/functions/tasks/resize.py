from PIL import Image

from imgmanip.functions.save_img import save_image_path
from imgmanip.models.resize_type import ResizeType
from imgmanip.models.save_type import SaveType
from imgmanip.models.task import ResizeTask


def resize_image(image, resize_task: ResizeTask, save_type: SaveType, out_path=None):
    # Image
    img = Image.open(image)
    width, height = img.size

    new_file_name = save_image_path(image_path=image, save_type=save_type, out_path=out_path)

    if resize_task.resize_type == ResizeType.SIZE:
        img = img.resize((int(resize_task.new_width), int(resize_task.new_height)))
    elif resize_task.resize_type == ResizeType.PERCENTAGE:
        img = img.resize((int((resize_task.percent / 100) * width), int((resize_task.percent / 100) * height)))
    # img = img.resize((int(resize_task.new_width), int(resize_task.new_height)))

    img.save(new_file_name)
    return new_file_name
