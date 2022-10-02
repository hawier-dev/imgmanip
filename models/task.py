from models.image_extension import ImageExtension


class Task:
    def __init__(self):
        pass


class ResizeTask(Task):
    def __init__(self, new_width: int, new_height: int):
        super().__init__()
        self.name = 'resize'
        self.new_width = new_width
        self.new_height = new_height


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
    def __init__(self, from_color: str, to_color: str, save_mask: bool, save_shp: bool, save_geojson: bool):
        super().__init__()
        self.name = 'color_detection'
        self.from_color = from_color
        self.to_color = to_color
        self.save_mask = save_mask
        self.save_shp = save_shp
        self.save_geojson = save_geojson
