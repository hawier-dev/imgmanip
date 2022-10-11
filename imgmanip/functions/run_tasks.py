from imgmanip.functions.tasks.color_detection import detect_color
from imgmanip.functions.tasks.compress import compress_image
from imgmanip.functions.tasks.convert import convert_image
from imgmanip.functions.tasks.convert_color_mode import convert_color_mode_image
from imgmanip.functions.tasks.flip import flip_image
from imgmanip.functions.tasks.invert import invert_image
from imgmanip.functions.tasks.resize import resize_image
from imgmanip.models.task import InvertTask, ResizeTask, FlipTask, ConvertTask, CompressTask, ColorDetectionTask


def run_task(index, images_list, list_of_tasks, save_type, out_path):
    image = images_list[index]
    tasks_functions = {
        'resize': resize_image,
        'invert': invert_image,
        'flip': flip_image,
        'convert': convert_image,
        'compress': compress_image,
        'color_detection': detect_color,
        'convert_color_mode': convert_color_mode_image,
    }

    for task in list_of_tasks:
        try:
            file_name = tasks_functions[task.name](image, task, save_type, out_path)
            image = file_name
        except Exception as e:
            print(e)
            return image
