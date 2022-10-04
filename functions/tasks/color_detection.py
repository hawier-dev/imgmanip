from os.path import basename

import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from functions.get_ext import get_ext_from_file
from models.save_type import SaveType
from models.task import ColorDetectionTask


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
        shp_file_name = out_path + '/' + basename(image).replace(image_ext, '.shp')
        geojson_file_name = out_path + '/' + basename(image).replace(image_ext, '.geojson')
    elif save_type == SaveType.IMAGE_PATH:
        new_file_name = image.replace(image_ext, f'_new{image_ext}')
        mask_file_name = image.replace(image_ext, f'_mask{image_ext}')
        shp_file_name = image.replace(image_ext, '.shp')
        geojson_file_name = image.replace(image_ext, '.geojson')
    else:
        new_file_name = image
        mask_file_name = image.replace(image_ext, f'_mask{image_ext}')
        shp_file_name = image.replace(image_ext, '.shp')
        geojson_file_name = image.replace(image_ext, '.geojson')

    # Saving mask
    if task.save_mask and save_type.OVERWRITE:
        cv2.imwrite(mask_file_name, mask)

    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 5)

    # Saving shapefile and geojson
    if task.save_shp or task.save_geojson:
        contours = [np.squeeze(contour) for contour in contours if len(contour) > 2]
        polygons = map(Polygon, contours)
        multipolygon = MultiPolygon(polygons)
        crs = 'epsg:4326'
        polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[multipolygon])

        if task.save_shp:
            polygon.to_file(filename=shp_file_name, driver="ESRI Shapefile")

        if task.save_geojson:
            polygon.to_file(filename=geojson_file_name, driver='GeoJSON')

    cv2.imwrite(new_file_name, img)
    return new_file_name
