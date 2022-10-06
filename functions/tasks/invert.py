import cv2
from PIL import Image

from dialogs.confirm_dialog import ConfirmDialog
from functions.save_img import save_image_path
from models.save_type import SaveType
from models.task import InvertTask


def invert_image(image, invert_task: InvertTask, save_type: SaveType, out_path=None):
    img = cv2.imread(image)
    inverted_image = cv2.bitwise_not(img)

    new_file_name = save_image_path(image_path=image, save_type=save_type, out_path=out_path)

    cv2.imwrite(new_file_name, inverted_image)
    return new_file_name
