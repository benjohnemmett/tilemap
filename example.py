from src.tilemap import TileMap

ll_top_left = (48.865, 2.305)
ll_bottom_right = (48.855, 2.285)
zoom = 14

map = TileMap(ll_top_left, ll_bottom_right, 14)
map.preload_tiles()
map.render_map()
map.show()
map.save("tour_eiffel.png")
