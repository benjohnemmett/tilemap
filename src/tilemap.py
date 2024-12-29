import math
from .tilemanager import TileManager
from PIL import Image, ImageDraw
from .util import *

class TileMap():
    """
    Renders a tile map
    """
    def __init__(self, ll_p1, ll_p2, zoom):
        self.nw_corner = (max(ll_p1[0], ll_p2[0]), min(ll_p1[1], ll_p2[1])) # north west corner
        self.sw_corner = (min(ll_p1[0], ll_p2[0]), max(ll_p1[1], ll_p2[1])) # south east corner
        self.zoom = zoom
        self.layer = "s"
        self.tile_size = 256 # TODO verify images are this size, or resize them
        self.tile_manager = TileManager()

        top_left_corner = lat_lon_to_tile(self.nw_corner[0], self.nw_corner[1], zoom)
        bottom_right_corner = lat_lon_to_tile(self.sw_corner[0], self.sw_corner[1], zoom)
        self.tile_x_extent = (top_left_corner[0], bottom_right_corner[0])
        self.tile_y_extent = (top_left_corner[1], bottom_right_corner[1])
        print(f"Map extent x:{self.tile_x_extent}, y:{self.tile_y_extent}")

        self.required_x_tiles = list(range(int(self.tile_x_extent[0]), int(self.tile_x_extent[1] + 1)))
        self.required_y_tiles = list(range(int(self.tile_y_extent[0]), int(self.tile_y_extent[1] + 1)))
        print(f"Tiles x:{self.required_x_tiles}, y:{self.required_y_tiles}")

        pixel_bottom_right_corner = self.tile_to_pixel(self.tile_x_extent[1], self.tile_y_extent[1])
        pixel_top_left_corner = self.tile_to_pixel(self.tile_x_extent[0], self.tile_y_extent[0])
        self.map_size = pixel_bottom_right_corner
        print(f"Map size x:{self.map_size[0]}, y:{self.map_size[1]}")

        # Calculate Pixel offset from tile top left corner
        self.pixel_shift_x = int(math.floor(self.tile_size * (int(top_left_corner[0]) - top_left_corner[0])))
        self.pixel_shift_y = int(math.floor(self.tile_size * (int(top_left_corner[1]) - top_left_corner[1])))
        print(f"Pixel shift x:{self.pixel_shift_x}, y:{self.pixel_shift_y}")

        self.image = Image.new("RGBA", (self.map_size[0], self.map_size[1]))
        self.draw = ImageDraw.Draw(self.image)

    def preload_tiles(self):
        """
        Loads tile images into cache
        """
        for i, x in enumerate(self.required_x_tiles):
            for j, y in enumerate(self.required_y_tiles):
                print(f"Loading tile ({x}, {y}, {self.zoom})")
                self.tile_manager.load_tile(x, y, self.zoom)

    def render_map(self):
        """
        Render tile images on main Image
        """
        for i, x in enumerate(self.required_x_tiles):
            for j, y in enumerate(self.required_y_tiles):
                tile = self.tile_manager.get_tile(x, y, self.zoom)
                if tile is None:
                    print(f"Skipping missing tile ({x}, {y}, {self.zoom})")
                    continue
                self.image.paste(tile, (self.pixel_shift_x + i * 256, self.pixel_shift_y + j * 256))
                # TODO cutoff tiles for the bottom & left edges
                #     or is this already done by the image size...?

    def mark_point(self, lat, lon, color=(255, 0, 0)):
        # Calculate tile coordinates
        tile_x, tile_y = lat_lon_to_tile(lat, lon, self.zoom)
        # Calculate pixel coordinates
        pixel_x, pixel_y = self.tile_to_pixel(tile_x, tile_y)
        
        self.draw.point((pixel_x, pixel_y), fill=color)

    def tile_to_pixel(self, x, y):
        pixel_x = int(self.tile_size * (x - self.tile_x_extent[0]))
        pixel_y = int(self.tile_size * (y - self.tile_y_extent[0]))
        return (pixel_x, pixel_y)

    def show(self):
        """
        Show main Image
        """
        self.image.show()

    def save(self, path):
        self.image.save(path)