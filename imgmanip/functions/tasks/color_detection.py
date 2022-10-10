from os.path import basename

import cv2
import numpy as np

from imgmanip.functions.get_ext import get_ext_from_file
from imgmanip.models.save_type import SaveType
from imgmanip.models.task import ColorDetectionTask


def detect_color(image, task: ColorDetectionTask, save_type: SaveType, out_path=None):
    img = cv2.imread(image)
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # From color
    lower = np.array(task.color, dtype="uint8")
    # To color
    upper = np.array(task.color, dtype="uint8")
    # Mask with color
    mask = cv2.inRange(img, lower, upper)
    image_ext = get_ext_from_file(image)

    if save_type == SaveType.SELECT_PATH:
        new_file_name = out_path + '/' + basename(image)
        mask_file_name = out_path + '/' + basename(image).replace(image_ext, f'_mask{image_ext}')
    elif save_type == SaveType.IMAGE_PATH:
        new_file_name = image.replace(image_ext, f'_new{image_ext}')
        mask_file_name = image.replace(image_ext, f'_mask{image_ext}')
    else:
        new_file_name = image
        mask_file_name = image.replace(image_ext, f'_mask{image_ext}')

    # Saving mask
    if task.save_mask and save_type.OVERWRITE:
        cv2.imwrite(mask_file_name, mask)

    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 5)

    cv2.imwrite(new_file_name, img)
    return new_file_name
