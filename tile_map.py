import math
import os
from PIL import Image, ImageDraw
import map_it.util as util

class TileMap():
    def __init__(self, ll_p1, ll_p2, zoom):
        self.nw_corner = (max(ll_p1[0], ll_p2[0]), min(ll_p1[1], ll_p2[1])) # north west corner
        self.sw_corner = (min(ll_p1[0], ll_p2[0]), max(ll_p1[1], ll_p2[1])) # south east corner
        self.zoom = zoom
        self.missing_tiles_list = []
        self.tile_cache = {}
        self.tile_size = 256 # TODO verify images are this size, or resize them

        top_left_corner = util.lat_lon_to_tile(self.nw_corner[0], self.nw_corner[1], zoom)
        bottom_right_corner = util.lat_lon_to_tile(self.sw_corner[0], self.sw_corner[1], zoom)
        self.tile_x_extent = (top_left_corner[0], bottom_right_corner[0])
        self.tile_y_extent = (top_left_corner[1], bottom_right_corner[1])
        print(f"Map extent x:{self.tile_x_extent}, y:{self.tile_y_extent}")

        x_tiles = list(range(int(self.tile_x_extent[0]), int(self.tile_x_extent[1] + 1)))
        y_tiles = list(range(int(self.tile_y_extent[0]), int(self.tile_y_extent[1] + 1)))
        print(f"Tiles x:{x_tiles}, y:{y_tiles}")

        pixel_bottom_right_corner = self.tile_to_pixel(self.tile_x_extent[1], self.tile_y_extent[1])
        pixel_top_left_corner = self.tile_to_pixel(self.tile_x_extent[0], self.tile_y_extent[0])
        self.map_size = pixel_bottom_right_corner
        print(f"Map size x:{self.map_size[0]}, y:{self.map_size[1]}")

        self.image = Image.new("RGBA", (self.map_size[0], self.map_size[1]))
        self.draw = ImageDraw.Draw(self.image)

        # Fetch the tiles
        for i, x in enumerate(x_tiles):
            for j, y in enumerate(y_tiles):
                print(f"Getting tile ({x}, {y}, {zoom})")
                tile_path = util.get_tile_path(x, y, zoom)
                tile_exists_on_file = tile_path is not None
                if tile_exists_on_file:
                    tile = Image.open(tile_path)
                    self.tile_cache[(x, y, zoom)] = tile
                else:
                    self.missing_tiles_list.append((x, y, zoom))
                    util.fetch_tile(x, y, zoom) # TODO make this optional

        # Calculate Pixel offset from tile top left corner
        self.pixel_shift_x = int(math.floor(self.tile_size * (int(top_left_corner[0]) - top_left_corner[0])))
        self.pixel_shift_y = int(math.floor(self.tile_size * (int(top_left_corner[1]) - top_left_corner[1])))
        print(f"Pixel shift x:{self.pixel_shift_x}, y:{self.pixel_shift_y}")

        for i, x in enumerate(x_tiles):
            for j, y in enumerate(y_tiles):
                if (x, y, zoom) not in self.tile_cache:
                    print(f"Skipping missing tile ({x}, {y}, {zoom})")
                    continue
                tile = self.tile_cache[(x, y, zoom)]
                self.image.paste(tile, (self.pixel_shift_x + i * 256, self.pixel_shift_y + j * 256))
                # TODO cutoff tiles for the bottom & left edges
                #     or is this already done by the image size...?

    def mark_point(self, lat, lon, color=(255, 0, 0)):
        # Calculate tile coordinates
        tile_x, tile_y = util.lat_lon_to_tile(lat, lon, self.zoom)
        # Calculate pixel coordinates
        pixel_x, pixel_y = self.tile_to_pixel(tile_x, tile_y)
        
        self.draw.point((pixel_x, pixel_y), fill=color)

    def tile_to_pixel(self, x, y):
        pixel_x = int(self.tile_size * (x - self.tile_x_extent[0]))
        pixel_y = int(self.tile_size * (y - self.tile_y_extent[0]))
        return (pixel_x, pixel_y)

    def show(self):
        self.image.show()

    def save(self, path):
        self.image.save(path)