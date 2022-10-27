from imgmanip.functions.tasks.color_detection import detect_color
from imgmanip.functions.tasks.compress import compress_image
from imgmanip.functions.tasks.convert import convert_image
from imgmanip.functions.tasks.convert_color_mode import convert_color_mode_image
from imgmanip.functions.tasks.flip import flip_image
from imgmanip.functions.tasks.invert import invert_image
from imgmanip.functions.tasks.resize import resize_image
import pyexiv2


def run_task(index, images_list, list_of_tasks, save_type, out_path):
    image = images_list[index]
    old_image = pyexiv2.Image(image)
    image_exif = old_image.read_exif()
    image_xmp = old_image.read_xmp()
    image_iptc = old_image.read_iptc()
    old_image.close()

    tasks_functions = {
        "resize": resize_image,
        "invert": invert_image,
        "flip": flip_image,
        "convert": convert_image,
        "compress": compress_image,
        "color_detection": detect_color,
        "convert_color_mode": convert_color_mode_image,
    }

    for task in list_of_tasks:
        try:
            file_name = tasks_functions[task.name](image, task, save_type, out_path)
            image = file_name
        except Exception as e:
            print(e)
            return image

    new_image = pyexiv2.Image(image)
    new_image.modify_exif(image_exif)
    new_image.modify_xmp(image_xmp)
    new_image.modify_iptc(image_iptc)
    new_image.close()
