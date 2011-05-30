from classes import terrain_mapper
from rules import map_data, region_data
from pages import common

page_data = {
	"Title":	"World of Arl Map",
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	grid_size	= int(common.get_val('grid_size', 0))
	region		= common.get_val('region', 'rayti')
	
	if grid_size not in [10, 20, 30, 40, 60, 80, 100]:
		grid_size = 10
	
	the_map = terrain_mapper.Terrain_mapper()
	the_map.mouseover = 0
	the_map.grid_size = grid_size
	region_source_dict = region_data.get_source_dict(the_map, region, build_mode=0)
	
	if common.get_val('mode') == "terrain_map":
		map_output = the_map.map_terrain(cursor, colour_mode=True)
	else:
		map_output = the_map.map_terrain(cursor)
	
	terrain_select_list = []
	for t in map_data.terrain:
		terrain_select_list.append("<option value='%s'>%s</option>" % (t, t))
	
	terrain_select = "".join(terrain_select_list)
	
	source_dict = {
		"onclick_js":			"",
		"pgrid_size":			int(grid_size*2.5),
		"output":				map_output,
		"map_legend":			"",
		
		"header":				"""<div style="background-image: url('%(media_path)simages/grid_%(pgrid_size)s.png'); position: absolute; top:0px; left:0px; width:%(map_width)spx; height:%(map_height)spx;" onclick="alert('The background recieved an onclick, this is probably not meant to happen.');"></div>""" % {
			"pgrid_size":	int(grid_size*2.5),
			"map_width":	(the_map.right - the_map.left)*2.5,
			"map_height":	(the_map.bottom - the_map.top)*2.5,
			"media_path":	common.data['media_path'],
		},
		
		"footer":				"""<div style="position:absolute;top:%(map_height)spx;width:%(map_width)spx;height:30px;background-color:#ACF;">
			<select name="terrain" id="terrain">
				%(terrain_select)s
			</select>
			&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=10%(region)s">Minute</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=20%(region)s">Tiny</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=30%(region)s">Small</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=40%(region)s">Normal</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=60%(region)s">Big</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=80%(region)s">Large</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=edit_map&amp;grid_size=100%(region)s">Huge</a>&nbsp;&nbsp;&nbsp;
		</div>""" % {
			"map_width":		(the_map.right - the_map.left)*2.5,
			"map_height":		(the_map.bottom - the_map.top)*2.5,
			"region":			"&amp;region=%s" % region,
			"terrain_select":	terrain_select,
		}
	}
	
	for k, v in region_source_dict.items():
		source_dict[k] = v
	
	output = terrain_mapper.map_source(source_dict)
	return output