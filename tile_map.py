import os
from PIL import Image, ImageDraw
import map_vis.util as util

class TileMap():
    def __init__(self, ll_p1, ll_p2, zoom):
        self.p1 = (max(ll_p1[0], ll_p2[0]), min(ll_p1[1], ll_p2[1])) # north west corner
        self.p2 = (min(ll_p1[0], ll_p2[0]), max(ll_p1[1], ll_p2[1])) # south east corner
        self.zoom = zoom
        self.missing_tiles_list = []
        self.tiles = {}
        tile_size = 256 # TODO get this from images... or at least verify it

        x1, y1 = util.lat_lon_to_tile(self.p1[0], self.p1[1], zoom)
        x2, y2 = util.lat_lon_to_tile(self.p2[0], self.p2[1], zoom)
        self.x_extent = sorted((x1, x2)) # TODO is it necessasry to sort here, it's already forced into topleft/bottomright
        self.y_extent = sorted((y1, y2))
        print(f"Map extent x:{self.x_extent}, y:{self.y_extent}")

        # TODO  would be better to store as lists of tile numbers instead of ranges
        x_tiles = range(int(self.x_extent[0]), int(self.x_extent[1] + 1) + 1)
        y_tiles = range(int(self.y_extent[0]), int(self.y_extent[1] + 1) + 1)

        self.map_size = [int(tile_size * (self.x_extent[1] - self.x_extent[0])), 
                               int(tile_size * (self.y_extent[1] - self.y_extent[0]))]
        self.image = Image.new("RGBA", (self.map_size[0], self.map_size[1]))

        # Fetch the tiles
        for i, x in enumerate(x_tiles):
            for j, y in enumerate(y_tiles):
                print(f"Getting tile ({x}, {y}, {zoom})")
                tile_path = util.get_tile_path(x, y, zoom)
                tile_exists_on_file = tile_path is not None
                if tile_exists_on_file:
                    tile = Image.open(tile_path)
                    print(f"  size: {tile.size}")
                    self.tiles[(x, y, zoom)] = tile
                else:
                    self.missing_tiles_list.append((x, y, zoom))
                    util.fetch_tile(x, y, zoom)

        # Draw the tiles
        top_left = util.lat_lon_to_tile(self.p1[0], self.p1[1], zoom)

        # Top left coordinate
        x_shift_pixels = int(tile_size * (int(top_left[0]) - top_left[0]))
        y_shift_pixels = int(tile_size * (int(top_left[1]) - top_left[1]))
        print(f"Pixel shift x:{x_shift_pixels}, y:{y_shift_pixels}")
        for i, x in enumerate(x_tiles):
            for j, y in enumerate(y_tiles):
                if (x, y, zoom) not in self.tiles:
                    print(f"Skipping missing tile ({x}, {y}, {zoom})")
                    continue
                tile = self.tiles[(x, y, zoom)]
                self.image.paste(tile, (x_shift_pixels + i * 256, y_shift_pixels + j * 256))
                # TODO cutoff tiles for the bottom & left edges
                #     or is this already done by the image size...?
            

        # self.image.show(title=f"Map (zoom {zoom})")
        # self.image.save(f"map_{zoom}.png")

    # TODO implement this
    def mark_point(self, lat, lon, color=(255, 0, 0)):
        pass

    def show(self):
        self.image.show()

    def save(self, path):
        self.image.save(path)