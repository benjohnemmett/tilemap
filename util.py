import math
import os
import requests

util_file_path = os.path.abspath(__file__)
map_vis_tile_dir_path = os.path.join(os.path.dirname(util_file_path), "map_tiles")
print(f"map_vis_tile_dir_path: {map_vis_tile_dir_path}")

# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
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

def get_tile_url(x, y, zoom):
#   return f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
  return f"https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={zoom}"

def get_tile_path(x, y, zoom, map_tile_dir=map_vis_tile_dir_path):
  file_name = f"s-{zoom}-{x}-{y}.jpeg"
  file_path = os.path.join(map_tile_dir, file_name)
  if os.path.exists(file_path):
    return file_path
  return None

def fetch_tile_lat_lon(lat, lon, zoom, map_tile_dir=map_vis_tile_dir_path ):
  x, y = lat_lon_to_tile_int(lat, lon, zoom=zoom)
  return fetch_tile(x, y, zoom, map_tile_dir=map_tile_dir)

def fetch_tile(x, y, zoom, map_tile_dir=map_vis_tile_dir_path):
  file_name = f"s-{zoom}-{x}-{y}.jpeg"
  url = get_tile_url(x, y, zoom)
  print(f"Fetching {url}")
  response = requests.get(url)
  if response.status_code == 200:
    print(f"Saving {file_name}")
    with open(os.path.join(map_tile_dir, file_name), 'wb') as f:
      f.write(response.content)
  else:
    print(f"Failed to fetch {url} with status code {response.status_code}")