import os

import cv2
from PIL import Image

# from models.task import TaskModel
import numpy as np


def detect_color(image):  # , task: TaskModel, overwrite):
    img = cv2.imread(image)
    from_color = [0, 0, 0]
    to_color = [1, 1, 1]
    lower = np.array(from_color, dtype="uint8")
    upper = np.array(to_color, dtype="uint8")
    mask = cv2.inRange(img, lower, upper)
    cv2.imwrite('mask.png', mask)

    # TODO: Detect points with specified color
    # TODO: Saving mask
    # Overwrite old files
    # if overwrite:
    #     os.remove(image)
    #     return image
    #
    # img.save(image)
    # return image
