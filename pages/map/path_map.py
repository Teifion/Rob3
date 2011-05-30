from classes import mapper
from rules import map_data
from pages import common
from functions import path_f

page_data = {
	"Title":	"World of Arl Map",
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	points			= common.get_val('points', "")
	move_speed		= common.get_val('move_speed', "Marching")
	move_type		= common.get_val('move_type', "Medium foot")
	
	if points == "":
		page_data['Header'] = True
		page_data['Title'] = "Path map"
		
		# name, elements = {}, element_order = [], tab_index = -1, onchange="", custom_id = "<>", selected=""
		speed_dropdown = common.option_box('move_speed', map_data.move_speed_list, selected="Marching")
		type_dropdown = common.option_box('move_type', map_data.move_type_list, selected="Medium foot")
		
		return """
		<form action="web.py" method="get" accept-charset="utf-8" style="padding:5px;">
			<input type="hidden" name="mode" value="path_map" />
			<table border="0" cellspacing="0" cellpadding="5">
				<tr>
					<td><label for="points">Waypoints:</label></td>
					<td><input type="text" id="points" name="points" value="" size="40"/></td>
				</tr>
				<tr>
					<td><label for="move_speed">Speed:</label></td>
					<td>
						{move_speed}
					</td>
				</tr>
				<tr>
					<td><label for="move_type">Type:</label></td>
					<td>
						{move_type}
					</td>
				</tr>
				<tr>
					<td><input type="submit" value="View" /></td>
					<td>&nbsp;</td>
				</tr>
			</table>
		</form>
		{onload}
		""".format(
			move_speed=speed_dropdown,
			move_type=type_dropdown,
			onload=common.onload("$('#points').focus();")
		)
	
	try:
		move_speed		= map_data.move_speed_list[int(move_speed)]
	except Exception as e:
		pass
	
	try:
		move_type		= map_data.move_type_list[int(move_type)]
	except Exception as e:
		pass
	
	waypoints = []
	points_list = points.split(",")
	for p in range(0, len(points_list), 2):
		waypoints.append((int(points_list[p]), int(points_list[p+1])))

	path_data = path_f.path(cursor, waypoints, move_speed=move_speed, move_type=move_type)
	
	
	float_div = """<div style="background-color:#CCC;position:absolute;top:0px;left:0px;padding:5px;">
	<a href="web.py?mode=path_map">Reset</a><br />
	Distance: {distance}<br />
	Time taken: {time}<br />
	</div>""".format(
		distance = format(path_data.walk_distance, ','),
		time = path_data.time_cost,
	)
	
	
	dimensions = {
		"left":		999999,
		"top":		999999,
		"right":	-999999,
		"bottom":	-999999,
	}

	# Need to work out how big the map will actually be
	radius = 300
	for s in path_data.steps:
		dimensions['left'] = min(dimensions['left'], s['tile'][0] - radius)
		dimensions['right'] = max(dimensions['right'], s['tile'][0] + radius)
	
		dimensions['top'] = min(dimensions['top'], s['tile'][1] - radius)
		dimensions['bottom'] = max(dimensions['bottom'], s['tile'][1] + radius)

	# Make map object
	the_map = mapper.Map_maker()
	the_map.path_data = path_data

	the_map.left	= max(dimensions['left'], the_map.left)
	the_map.right	= min(dimensions['right'], the_map.right)

	the_map.top		= max(dimensions['top'], the_map.top)
	the_map.bottom	= min(dimensions['bottom'], the_map.bottom)


	onclick_js = """
	var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
	var map_y = parseInt(document.getElementById('labelHideY').innerHTML);

	use_map_xy(map_x, map_y);"""
	
	source_dict = {
		# "build":				False,
		"onclick_js":			onclick_js,
	
		# "map_click_handler":	map_click_handler,
	
		"output":				the_map.map_grid(cursor),
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

	return "%s%s" % (float_div, mapper.map_source(source_dict))