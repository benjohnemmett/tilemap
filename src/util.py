import math
import os

util_file_path = os.path.abspath(__file__)
map_vis_tile_dir_path = os.path.join(os.path.dirname(util_file_path), "map_tiles")

# From https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
def lat_lon_to_tile(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 1 << zoom
  xtile = (lon_deg + 180.0) / 360.0 * n
  ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
  return xtile, ytile

def tile_to_lat_lon(xtile, ytile, zoom):
  n = 1 << zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return lat_deg, lon_deg

def lat_lon_to_tile_int(lat_deg, lon_deg, zoom):
  x, y, = lat_lon_to_tile(lat_deg, lon_deg, zoom)
  return int(x), int(y)
