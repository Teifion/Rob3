from data import mapper
from data import resource
from rules import map_data
from pages import common

grid_size = int(common.get_val('grid_size', 0))
colour_list = common.get_val('list', 0)
grid_size = 10

the_map = mapper.Map_maker()
the_map.mouseover = 0
the_map.grid_size = grid_size

onclick_js = """
var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
var map_y = parseInt(document.getElementById('labelHideY').innerHTML);

use_map_xy(map_x, map_y);"""

source_dict = {
	"onclick_js":			onclick_js,
	"output":				the_map.map_colour(colour_list)
}

output = mapper.map_source(source_dict)

print(output)