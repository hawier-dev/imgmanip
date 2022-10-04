from time import time

from functions.color_detection import detect_color
from functions.compress import compress_image
from functions.convert import convert_image
from functions.flip import flip_image
from functions.invert import invert_image
from functions.resize import resize_image
from models.task import InvertTask, ResizeTask, FlipTask, ConvertTask, CompressTask, ColorDetectionTask


def run_task(index, images_list, list_of_tasks, save_type, out_path):
    image = images_list[index]

    for task in list_of_tasks:
        # RESIZE TASK
        if type(task) == ResizeTask:
            file_name = resize_image(image, task, save_type,
                                     out_path)
            image = file_name
        # INVERT TASK
        elif type(task) == InvertTask:
            file_name = invert_image(image, task, save_type,
                                     out_path)
            image = file_name
        # FLIP TASK
        elif type(task) == FlipTask:
            file_name = flip_image(image, task, save_type,
                                   out_path)
            image = file_name
        # CONVERT TASK
        elif type(task) == ConvertTask:
            file_name = convert_image(image, task, save_type,
                                      out_path)
            image = file_name
        # COMPRESS TASK
        elif type(task) == CompressTask:
            file_name = compress_image(image, task, save_type,
                                       out_path)
            image = file_name
        # COLOR DETECTION TASK
        elif type(task) == ColorDetectionTask:
            file_name = detect_color(image, task, save_type,
                                     out_path)
            image = file_name
