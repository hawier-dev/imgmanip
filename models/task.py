from enum import Enum


# class Task(Enum):
#     RESIZE = 'resize'
#     INVERT = 'invert'
#     CONVERT = 'convert'
#     COMPRESS = 'compress'


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
