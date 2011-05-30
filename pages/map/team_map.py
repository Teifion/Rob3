from pages import common
from classes import mapper
from rules import map_data
from queries import city_q, army_q

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	team_id	= int(common.get_val('team', 0))
	build	= int(common.get_val('build', 0))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'team_map', ajax=1)
	
	return _draw_map(cursor, team_id, build)

def _draw_map(cursor, team_id, build):
	minx, maxx = 999999, -9999999
	miny, maxy = 999999, -9999999
	
	city_dict = city_q.get_cities_from_team(cursor, team_id, include_dead=False)
	for city_id, the_city in city_dict.items():
		minx = min(minx, the_city.x)
		maxx = max(maxx, the_city.x)
		
		miny = min(miny, the_city.y)
		maxy = max(maxy, the_city.y)
	
	army_dict = army_q.get_armies_from_team(cursor, team_id, include_garrisons=False)
	for army_id, the_army in army_dict.items():
		minx = min(minx, the_army.x)
		maxx = max(maxx, the_army.x)
		
		miny = min(miny, the_army.y)
		maxy = max(maxy, the_army.y)
	
	centre = (int((maxx+minx)/2), int((maxy+miny)/2))
	radius = max((maxx-minx), (maxy-miny)) + 300
	
	the_map = mapper.Map_maker()
	the_map.centre = centre
	the_map.centre_radius = radius
	the_map.personalise	= [team_id]
	
	if build != 0:# Remote mode
		the_map.icon_path = '../map/images/teamIcons/'
	
	onclick_js = """
	var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
	var map_y = parseInt(document.getElementById('labelHideY').innerHTML);
	
	use_map_xy(map_x, map_y);"""
	
	source_dict = {
		"build":				build,
		"onclick_js":			onclick_js,
		
		"output":				the_map.map_grid(cursor),
		
		# 'map_path':				"../map/images/theMap.jpg",
		# 'jquery':				"../includes/jquery.js",
		# 'transparent_path':		"../map/images/trans75.png",
		# 'key_path':				"../map/images/key.png",
	}
	
	source_dict['map_legend']	= ''
	
	source_dict["left"]			= the_map.left * 2.5
	source_dict["right"]		= the_map.right
	source_dict["top"]			= the_map.top * 2.5
	source_dict["bottom"]		= the_map.bottom
	
	source_dict["map_width"]	= the_map.width*2.5
	source_dict["map_height"]	= the_map.height*2.5
	
	x_diff = map_data.dimensions['left'] - the_map.left
	y_diff = map_data.dimensions['top'] - the_map.top
	source_dict["margin_left"]	= (x_diff + map_data.dimensions['margin_left'])*2.5
	source_dict["margin_top"]	= (y_diff + map_data.dimensions['margin_top'])*2.5
	
	if build:
		source_dict['map_path']			= '../map/images/theMap.jpg'
		source_dict['jquery']			= "../includes/jquery.js"
		source_dict['transparent_path']	= "../map/images/trans75.png"
		source_dict['key_path']			= "../map/images/key.png"
	
	output = mapper.map_source(source_dict)
	
	return output