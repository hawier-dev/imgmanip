import os

import cv2
from PIL import Image
import numpy as np

from functions.get_ext import get_ext_from_file
from models.task import ColorDetectionTask


def detect_color(image, task: ColorDetectionTask, overwrite):
    img = cv2.imread(image)
    # From color
    lower = np.array(task.from_color, dtype="uint8")
    # To color
    upper = np.array(task.to_color, dtype="uint8")
    # Mask with color
    mask = cv2.inRange(img, lower, upper)
    image_ext = get_ext_from_file(image)
    mask_file_name = image.replace(image_ext)

    # Saving mask
    if task.save_mask:
        cv2.imwrite(mask_file_name, mask)

    # Saving shapefile and geojson
    if task.save_shp or task.save_geojson:
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Overwrite old files
    if overwrite:
        os.remove(image)
        return image

    img.save(image)
    return image
