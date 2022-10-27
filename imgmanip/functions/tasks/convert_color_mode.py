from PIL import Image

from imgmanip.functions.save_img import save_image_path
from imgmanip.models.save_type import SaveType
from imgmanip.models.task import ConvertColorModeTask


def convert_color_mode_image(
        image,
        convert_color_mode_task: ConvertColorModeTask,
        save_type: SaveType,
        out_path=None,
):
    img = Image.open(image).convert(convert_color_mode_task.color_mode.value)

    new_file_name = save_image_path(
        image_path=image, save_type=save_type, out_path=out_path
    )

    img.save(new_file_name)
    return new_file_name
