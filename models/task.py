from enum import Enum


class ImageExtension(Enum):
    JPEG = '.jpg'
    TIFF = '.tif'
    PNG = '.png'
    GIF = '.gif'
    BITMAP = '.bmp'


class Task:
    def __init__(self):
        pass


class TaskResize(Task):
    def __init__(self, new_width=None, new_height=None):
        super().__init__()
        self.new_width = new_width
        self.new_height = new_height


class TaskInvert(Task):
    def __init__(self):
        super().__init__()


class TaskConvert(Task):
    def __init__(self, convert_ext: ImageExtension):
        super().__init__()
        self.convert_ext = convert_ext


class TaskCompress(Task):
    def __init__(self, quality=90):
        super().__init__()
        self.quality = quality


class TaskColorDetection(Task):
    def __init__(self, from_color: str, to_color: str, save_mask: bool, save_shp: bool, save_geojson: bool):
        super().__init__()
        self.from_color = from_color
        self.to_color = to_color
        self.save_mask = save_mask
        self.save_shp = save_shp
        self.save_geojson = save_geojson
