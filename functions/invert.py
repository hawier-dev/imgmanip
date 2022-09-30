import cv2

from functions.get_ext import get_ext_from_file
from models.task import TaskInvert


def invert_image(image, invert_task: TaskInvert, overwrite):
    img = cv2.imread(image)
    inverted_image = cv2.bitwise_not(img)
    image_ext = get_ext_from_file(image)
    new_image_name = image.replace(image_ext, f'_new{image_ext}')

    if overwrite:
        cv2.imwrite(image, inverted_image)
        return image

    cv2.imwrite(new_image_name, inverted_image)
    return new_image_name
