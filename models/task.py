from models.axis import Axis
from models.image_extension import ImageExtension
from models.resize_type import ResizeType


class Task:
    def __init__(self):
        pass


class ResizeTask(Task):
    def __init__(self, resize_type: ResizeType, new_width=800, new_height=600, percent=100):
        super().__init__()
        self.name = 'resize'
        self.resize_type = resize_type
        self.new_width = new_width
        self.new_height = new_height
        self.percent = percent


class InvertTask(Task):
    def __init__(self):
        super().__init__()
        self.name = 'invert'


class ConvertTask(Task):
    def __init__(self, convert_ext: ImageExtension):
        super().__init__()
        self.name = 'convert'
        self.convert_ext = convert_ext


class CompressTask(Task):
    def __init__(self, quality=90):
        super().__init__()
        self.name = 'compress'
        self.quality = quality


class ColorDetectionTask(Task):
    def __init__(self, from_color: str, color: str, save_mask: bool, save_shp: bool, save_geojson: bool):
        super().__init__()
        self.name = 'color_detection'
        self.color = color
        self.save_mask = save_mask
        self.save_shp = save_shp
        self.save_geojson = save_geojson


class FlipTask(Task):
    def __init__(self, axis=Axis.HORIZONTAL):
        super().__init__()
        self.name = 'flip'
        self.axis = axis