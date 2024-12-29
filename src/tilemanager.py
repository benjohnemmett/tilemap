import os
import requests
from .util import *
from PIL import Image

class TileManager:
  """
  Downloads tile image files
  """

  def __init__(self, layer="s", map_tile_dir=map_vis_tile_dir_path):
    self.map_tile_dir=map_tile_dir
    self.layer = layer
    self.tile_cache = {}

    if not os.path.exists(map_tile_dir):
      os.mkdir(map_tile_dir)

  def get_tile(self, x, y, zoom):
    """
    Returns Image if tile is loaded or can be loaded. Otherwise returns None.
    """
    self.load_tile(x, y, zoom)

    tile_code = (x, y, zoom)
    if tile_code in self.tile_cache:
      return self.tile_cache[tile_code]
    
    return None

  def get_tile_url(self, x, y, zoom):
    return f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    # return f"https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={zoom}"

  def get_tile_path(self, x, y, zoom):
    file_name = f"{self.layer + '-' if self.layer else ''}{zoom}-{x}-{y}.jpeg"
    file_path = os.path.join(self.map_tile_dir, file_name)
    return file_path
  
  def load_tile(self, x, y, zoom):
    """
    Checks that tile image exists and loads it into the local cache if it does,
    otherwise it attempts to download the tile.

    Returns True if tile image is in cache, false otherwise
    """
    print(f"Getting tile ({x}, {y}, {zoom})")
    tile_code = (x, y, zoom)
    if tile_code in self.tile_cache:
      return True
    
    tile_path = self.get_tile_path(x, y, zoom)
    if os.path.exists(tile_path):
        tile = Image.open(tile_path)
        self.tile_cache[(x, y, zoom)] = tile
        return True
    else:
        if self.download_tile(x, y, zoom):
          try:
            tile = Image.open(tile_path)
            self.tile_cache[(x, y, zoom)] = tile
            return True
          except:
            return False # Error reading file
        else:
          return False # Download failed

  def download_tile_lat_lon(self, lat, lon, zoom):
    """
    Returns True if tile was downloaded successfully
    """
    x, y = lat_lon_to_tile_int(lat, lon, zoom=zoom)
    return self.download_tile(x, y, zoom)

  def download_tile(self, x, y, zoom):
    """
    Returns True if tile was downloaded successfully
    """
    file_name = self.get_tile_path(x, y, zoom)
    url = self.get_tile_url(x, y, zoom)
    print(f"Fetching {url}")
    response = requests.get(url)
    if response.status_code == 200:
      print(f"Saving {file_name}")
      with open(file_name, 'wb') as f:
        f.write(response.content)
      return True
    else:
      print(f"Failed to fetch {url} with status code {response.status_code}")
      print(response.content)
      return False