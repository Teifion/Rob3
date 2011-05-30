from classes import mapper
from rules import map_data
from pages import common

from rules import region_data

page_data = {
	"Title":	"World of Arl Map",
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	build		= int(common.get_val('build', 0))
	region_name	= common.get_val('region', '').lower()
	
	the_map = mapper.Map_maker()
	
	if build != 0:# Remote mode
		the_map.icon_path = 'images/teamIcons/'
	
	onclick_js = """
	var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
	var map_y = parseInt(document.getElementById('labelHideY').innerHTML);
	use_map_xy(map_x, map_y);"""
	
	source_dict = region_data.get_source_dict(the_map, region_name, build)
	source_dict["build"]		= build
	source_dict["onclick_js"]	= onclick_js
	source_dict["output"]		= the_map.map_grid(cursor)
	
	return mapper.map_source(source_dict)
