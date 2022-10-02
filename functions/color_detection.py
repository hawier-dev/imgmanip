import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
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
    # File names
    new_file_name = image.replace(image_ext, f'_new{image_ext}')
    mask_file_name = image.replace(image_ext, f'_mask{image_ext}')
    shp_file_name = image.replace(image_ext, '.shp')
    geojson_file_name = image.replace(image_ext, '.geojson')

    # Saving mask
    if task.save_mask:
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
            polygon.to_file(
                filename=shp_file_name, driver="ESRI Shapefile")

        if task.save_geojson:
            polygon.to_file(filename=geojson_file_name, driver='GeoJSON')

    # Overwrite old files
    if overwrite:
        cv2.imwrite(image, img)
        return image

    cv2.imwrite(new_file_name, img)
    return new_file_name
