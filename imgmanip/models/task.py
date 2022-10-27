from imgmanip.models.axis import Axis
from imgmanip.models.color_mode import ColorMode
from imgmanip.models.image_extension import ImageExtension
from imgmanip.models.resize_type import ResizeType


class Task:
    def __init__(self):
        pass


class ResizeTask(Task):
    def __init__(
        self, resize_type: ResizeType, new_width=800, new_height=600, percent=100
    ):
        super().__init__()
        self.name = "resize"
        self.resize_type = resize_type
        self.new_width = new_width
        self.new_height = new_height
        self.percent = percent
        self.name_extended = f"Resize: {new_width}x{new_height}"


class InvertTask(Task):
    def __init__(self):
        super().__init__()
        self.name = "invert"
        self.name_extended = f"Invert"


class ConvertTask(Task):
    def __init__(self, convert_ext: ImageExtension):
        super().__init__()
        self.name = "convert"
        self.convert_ext = convert_ext
        self.name_extended = f"Convert: {convert_ext.value}"


class CompressTask(Task):
    def __init__(self, quality=90):
        super().__init__()
        self.name = "compress"
        self.quality = quality
        self.name_extended = f"Compress: {quality}"


class ColorDetectionTask(Task):
    def __init__(self, save_mask: bool, color=None):
        super().__init__()
        self.name = "color_detection"
        self.color = color
        self.save_mask = save_mask
        self.name_extended = f"Color detection: {color}"


class FlipTask(Task):
    def __init__(self, axis=Axis.HORIZONTAL):
        super().__init__()
        self.name = "flip"
        self.axis = axis
        self.name_extended = f"Flip: {axis.value}"


class ConvertColorModeTask(Task):
    def __init__(self, color_mode=ColorMode):
        super().__init__()
        self.name = "convert_color_mode"
        self.color_mode = color_mode
        self.name_extended = f"Convert color mode: {color_mode.value}"
