from classes import mapper
from rules import map_data
from pages import common

page_data = {
	"Title":	"World of Arl Map",
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	build = int(common.get_val('build', 0))
	centre = common.get_val('centre', "")
	centre_radius = common.get_val('radius', 0)
		
	return _draw_map(cursor, build, centre, centre_radius)
	
def _draw_map(cursor, build, centre, centre_radius):
	the_map = mapper.Map_maker()
	
	if centre != "":
		centre = centre.split(",")
		the_map.centre = (int(centre[0]), int(centre[1]))
		
		if centre_radius > 0:
			the_map.centre_radius = centre_radius
	
	if build != 0:# Remote mode
		the_map.icon_path = 'images/teamIcons/'
	
	onclick_js = """
	var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
	var map_y = parseInt(document.getElementById('labelHideY').innerHTML);
	
	use_map_xy(map_x, map_y);"""
	
	# new_mode is used when we want to select a location for something
	new_mode = common.get_val('new_mode', "")
	new_mode_form_fields = ""
	
	if new_mode == "edit_city":
		new_mode_form_fields = '<input type="hidden" name="city" value="%s" />' % int(common.get_val('city', ""))
		map_click_handler = "$('#new_mode_form').submit();"
	
	elif new_mode == "edit_army":
		new_mode_form_fields = '<input type="hidden" name="army" value="%s" />' % int(common.get_val('army', ""))
		map_click_handler = "$('#new_mode_form').submit();"
	
	elif new_mode =="list_armies" or new_mode =="list_cities":
		new_mode_form_fields = '<input type="hidden" name="team" value="%s" />' % int(common.get_val('team', ""))
		map_click_handler = "$('#new_mode_form').submit();"
	
	elif new_mode == "setup_battle":
		new_mode_form_fields = '<input type="hidden" name="battle" value="%s" />' % int(common.get_val('battle', ""))
		map_click_handler = "$('#new_mode_form').submit();"
	
	else:
		if new_mode != '':
			print("No handler for new_mode of '%s' in web.map.view_map" % new_mode)
			exit()
	
	source_dict = {
		"build":				build,
		"onclick_js":			onclick_js,
		
		"new_mode":				new_mode,
		# "map_click_handler":	map_click_handler,
		"new_mode_form_fields": new_mode_form_fields,
		
		"output":				the_map.map_grid(cursor),
	}
	
	if centre != "":
		source_dict['map_legend']	= ''
		
		source_dict["left"]			= the_map.left
		source_dict["right"]		= the_map.right
		source_dict["top"]			= the_map.top
		source_dict["bottom"]		= the_map.bottom
		
		source_dict["map_width"]	= the_map.width*2.5
		source_dict["map_height"]	= the_map.height*2.5
		
		x_diff = map_data.dimensions['left'] - the_map.left
		y_diff = map_data.dimensions['top'] - the_map.top
		source_dict["margin_left"]	= (x_diff + map_data.dimensions['margin_left'])*2.5
		source_dict["margin_top"]	= (y_diff + map_data.dimensions['margin_top'])*2.5
		
		# print("")
		# print(source_dict)
		
	try:
		if map_click_handler:
			source_dict['map_click_handler'] = map_click_handler
	except Exception:
		pass
	
	return mapper.map_source(source_dict)