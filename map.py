import os
from PIL import Image, ImageDraw
from util import lat_lon_to_tile, tile_to_lat_lon, map_vis_tile_dir_path

class Map():
  def __init__(self, x, y, zoom, map_tile_dir=map_vis_tile_dir_path):
    self.map_tile_dir = map_tile_dir

    start_lat, start_lon = tile_to_lat_lon(x, y, zoom)
    end_lat, end_lon = tile_to_lat_lon(x+1, y+1, zoom)
    self.lat_extent = sorted((start_lat, end_lat))
    self.lon_extent = sorted((start_lon, end_lon))

    self.zoom = zoom
    file_name = f"s-{zoom}-{x}-{y}.jpeg"
    self.image = Image.open(os.path.join(self.map_tile_dir,file_name))
    self.image = self.image.convert("RGBA")
    self.image_w = self.image.size[0]
    self.image_h = self.image.size[1]
    self.draw = ImageDraw.Draw(self.image)
    print(f"Loaded image {file_name} with width {self.image_w} and height {self.image_h} and mode {self.image.mode}") 

  def mark(self, lat, lon):
    if lat < self.lat_extent[0] or lat > self.lat_extent[1] or lon < self.lon_extent[0] or lon > self.lon_extent[1]:
      print("Marker out of bounds")
      return
    x, y = lat_lon_to_tile(lat, lon, self.zoom)
    marker_x = int((x % 1.0) * self.image_w)
    marker_y = int((y % 1.0) * self.image_h)
    self.draw.point((marker_x, marker_y), fill=((255, 255, 0, 255)))

  def show(self):
    self.image.show()

