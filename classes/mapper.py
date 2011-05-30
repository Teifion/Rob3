import sys
import re
import database
import math
from queries import team_q, mapper_q, army_q, building_q
from queries import city_q, artefact_q, wonder_q
from functions import resource_f, city_f
# from functions import city_f

# from data import city
# from data import mapper_q, mapper_f
# from data import resource
# 
# from data import building, artefact, wonder
# from data import army_q
from rules import map_data, map_resources
from lists import resource_list
from pages import common

res_names = {}
for i, r in enumerate(resource_list.data_list):
	res_names[i] = r.name.lower().replace(" ", "")

safe_re = re.compile(r"[^a-zA-Z_0-9]")

def map_control_size(size_value):
	if size_value < 1: return 0
	
	# image_size = round(math.sqrt(size_value)/4.0)
	image_size = round(math.sqrt(size_value))
	
	# image_size = min(image_size, icon_max_size)
	# image_size = max(image_size, icon_min_size)
	
	return image_size

def terrain_tuples(cursor, force_requery=False):
	"""docstring for terrain_tuples"""
	if cache.terrain_tuples != {} and force_requery == False:
		return cache.terrain_tuples
	
	cache.terrain_tuples = mapper_q.get_terrain_tuples(cursor,
		top = map_data.dimensions['top'],
		right = map_data.dimensions['right'],
		bottom = map_data.dimensions['bottom'],
		left = map_data.dimensions['left'])
	
	return cache.terrain_tuples

class Map_terrain (database.DB_connected_object):
	table_info = {
		"Name":			"map_terrain",
		"Indexes":		{
		},
		"Fields":		(
			database.Integer_field("x",				primary_key=True),
			database.Integer_field("y",				primary_key=True),
			
			database.Integer_field("terrain"),
		),
	}
	
	def __init__(self, row = {}):
		super(Map_terrain, self).__init__(row)

class Map_continent (database.DB_connected_object):
	table_info = {
		"Name":			"map_continents",
		"Indexes":		{
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=50),
			
			database.Integer_field("x"),
			database.Integer_field("y"),
		),
	}
	
	def __init__(self, row = {}):
		super(Map_continent, self).__init__(row)
		
# Tiles on continent
Map_continent_tiles = {
	"Name":			"map_continent_tiles",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("continent",		primary_key=True, foreign_key=("map_continents", "id")),
		
		database.Integer_field("x",				primary_key=True),
		database.Integer_field("y",				primary_key=True),
	),
}


class Map_maker (object):
	"""docstring for ClassName"""
	def __init__(self):
		super(Map_maker, self).__init__()
		self.left			= map_data.dimensions['left']
		self.right			= map_data.dimensions['right']
		self.top			= map_data.dimensions['top']
		self.bottom			= map_data.dimensions['bottom']
		
		self.width			= 0
		self.height			= 0
		
		self.config			= {}
		self.append_last	= []
		self.city_dict		= {}
		self.team_dict		= {}
		# self.team_dict = team_q.get_real_active_teams(cursor, skip_irs=False)
		self.army_dict		= {}
		
		self.wonder_dict	= {}
		self.building_dict	= {}
		
		self.personalise	= []
		
		self.icon_path		= 'http://localhost/WoA/map/images/teamIcons/'
		self.mouseover		= 1
		self.grid_size		= 20
		self.draw_armies	= False
		
		self.centre			= None
		self.centre_radius	= 300
		
		self.path_data		= None
		self.gm				= False
	
	def check_size(self):
		if self.centre:
			self.left = max(self.left, self.centre[0] - self.centre_radius)
			self.right = min(self.right, self.centre[0] + self.centre_radius)
			
			self.top = max(self.top, self.centre[1] - self.centre_radius)
			self.bottom = min(self.bottom, self.centre[1] + self.centre_radius)
			
			# print("")
			# print("Left: %s<br />Right: %s<br />Top: %s<br />Bottom: %s<br />Centre: %s<br />Radius: %s<br />" % (self.left, self.right, self.top, self.bottom, self.centre, self.centre_radius))
			# exit()
		
		self.width = self.right - self.left
		self.height = self.bottom - self.top
	
	def map_grid(self, cursor):
		self._setup_grid(cursor)
		
		output = self._map_grid(cursor)
		
		return output
	
	def _setup_grid(self, cursor):
		self.check_size()
		
		# Teams
		self.team_dict = team_q.get_real_active_teams(cursor, skip_irs=False)
		
		# Cities
		self.city_dict = city_q.get_cities_for_map(cursor,
			left=self.left, top=self.top, right=self.right, bottom=self.bottom)
		
		# Buildings
		self.building_dict = building_q.get_all_buildings(cursor)
		
		# Very small saving
		city_q.mass_get_city_buildings(cursor, self.city_dict)
		
		# Huge time saving on this one
		city_f.mass_city_wall_check(cursor, self.city_dict)
		
		# Wonders
		self.wonder_dict = wonder_q.get_all_wonders(cursor)
		
		# Artefacts
		self.artefact_dict = artefact_q.get_all_artefacts(cursor)
		
		# Cache things so we don't need to iterate through all cities
		self.cities_with_wonder = []
		self.cities_with_artefact = []
		
		for k, v in self.wonder_dict.items():
			self.cities_with_wonder.append(v.city)
		
		for k, v in self.artefact_dict.items():
			self.cities_with_artefact.append(v.city)
		
		self.cities_with_wonder = set(self.cities_with_wonder)
		self.cities_with_artefact = set(self.cities_with_artefact)
	
	def _map_grid(self, cursor):
		output = []
		
		# Cities
		for c in self.city_dict.keys():
			output.append(self.draw_city(cursor, c))
		
		# Armies
		if self.draw_armies == True or len(self.personalise):
			self.army_dict = army_q.get_all_non_garrisons(cursor)
			
			for a in self.army_dict.keys():
				if self.draw_armies:
					self.army_dict[a].get_size(cursor)
					output.append(self.draw_army(a))
				
				elif self.army_dict[a].team in self.personalise:
					# Draw only the armies from a given set of teams
					self.army_dict[a].get_size(cursor)
					output.append(self.draw_army(a))
		
		# Path data
		if self.path_data != None:
			output.append(self.draw_path())

		# Append last!
		output.append("".join(self.append_last))
		
		return "".join(output)
	

	def draw_path(self):
		output = []
		
		for i, s in enumerate(self.path_data.steps):
			if s['tile'] == self.path_data.end_point: continue
			x, y = s['tile']
			
			output.append("""
		<div class="colour_box" style="top:{y}px; left:{x}px; width:{size}px; height:{size}px;">
			{content}
		</div>""".format(
			x		= (x - self.left) * 2.5,
			y		= (y - self.top) * 2.5,
			size	= 25,
			content	= i,
		))
		
		output.append("""
		<div class="colour_box" style="background-color:#FFF;color:#000;top:{y}px; left:{x}px; width:{size}px; height:{size}px;">
			{content}
		</div>""".format(
			x		= (self.path_data.end_point[0] - self.left) * 2.5,
			y		= (self.path_data.end_point[1] - self.top) * 2.5,
			size	= 25,
			content	= "F",
		))

		return "".join(output)


	def draw_army(self, army_id):
		the_army = self.army_dict[army_id]
		the_team = self.team_dict[the_army.team]
		
		if the_army.size < 1:
			return ""
		
		clean_name = the_team.clean_name()
		team_logo = '%s_army.png' % clean_name
		
		# Test for 1 icon		
		image_size = 40
		
		my_left		= (the_army.x - self.left) * 2.5 - (image_size/2)
		my_top		= (the_army.y - self.top) * 2.5 - (image_size/2)
		
		#	Mouseover
		#------------------------
		# Name
		clean_name = the_army.name.lower().replace(' ', '').replace("'", "")
		
		# Location
		army_x = the_army.x
		army_y = the_army.y
		
		army_title = ["<strong>Team</strong>: %s<br />" % the_team.name]
		
		# Size
		army_title.append("Size: %s" % the_army.size)
		
		# Output
		output = """<img class="army_icon" id="%(clean_name)s" src="%(icon_path)s%(team_logo)s" style="top:%(top)spx; left: %(left)spx;" width="%(image_size)s" height="%(image_size)s" onmouseover="$('#%(clean_name)s_hover').fadeIn(250);return False;" onmouseout="$('#%(clean_name)s_hover').hide(250);"/>""" %  {
			"icon_path":		self.icon_path,
			"clean_name":		clean_name,
			"top":				my_top,
			"left":				my_left,
			"image_size":		image_size,
			"team_logo":		team_logo,
		}
		
		if self.mouseover == 1:
			hover_top = my_top - 5
			hover_left = my_left + image_size + 20
			hover_left = max(hover_left, 5)
			
			if hover_left > ((self.width * 2.5) - 350):
				hover_left = my_left - 350
			
			# Floater
			self.append_last.append("""<div id="%(clean_name)s_hover" class="army_hover" style="top:%(hover_top)spx; left:%(hover_left)spx;"><div class="army_title">%(name)s&nbsp;&nbsp;&nbsp;%(army_x)s,%(army_y)s</div>%(army_title)s</div>""" % {
				"name": the_army.name,
				"clean_name": clean_name,
				"hover_top": hover_top,
				"hover_left": hover_left,
				"army_x": the_army.x,
				"army_y": the_army.y,
				"army_title": "".join(army_title),
			})
		
		# Now return it
		return "".join(output)
	
	def draw_city(self, cursor, city_id):
		city_is_special = False
		
		# Handles
		the_city = self.city_dict[city_id]
		the_team = self.team_dict[the_city.team]
		
		team_clean_name = the_team.clean_name()
		
		# Test for 1 icon	
		image_size = map_data.map_image_size(the_city.size)
		if image_size == 0:
			return ""
		
		my_left		= (the_city.x - self.left) * 2.5 - (image_size/2.0)
		my_top		= (the_city.y - self.top) * 2.5 - (image_size/2.0)
		
		# Check it's within the picture size of the map
		if (the_city.x - image_size/2) < self.left:		return ""
		if (the_city.x + image_size/2) > self.right:	return ""
		
		if (the_city.y - image_size/2) < self.top:		return ""
		if (the_city.y + image_size/2) > self.bottom:	return ""
		
		#	Mouseover
		#------------------------
		# Name
		# clean_name = the_city.name.lower().replace(' ', '').replace("'", "")
		# clean_name = common.js_name(the_city.name.lower().replace(' ', '').replace("'", ''))
		clean_name = safe_re.sub("", the_city.name)
		# safe_re
		
		# Location
		city_x = the_city.x
		city_y = the_city.y
		
		if the_team.ir:
			city_title = ["<strong>Team</strong>: %s <span style='font-size:0.9em;'>(IR)</span><br />" % the_team.name]
		else:
			city_title = ["<strong>Team</strong>: %s<br />" % the_team.name]
		
		# Port
		if the_city.port == True:
			city_title.append('Is a port')
		else:
			city_title.append('Not a port')
		
		# Nomadic
		if the_city.nomadic == True:
			city_title.append('<br />Nomadic')
		
		# Walls
		team_logo = '%s_unwalled.png' % team_clean_name
		has_harbour_walls = False
		
		# Harbour walls id = 18
		if 18 in the_city.buildings_amount and the_city.buildings_amount[18] > 0:
			has_harbour_walls = True
			city_title.append('<br />Harbour walls')
		
		if the_city.walls != []:
			if len(the_city.walls) > 1:
				if has_harbour_walls:
					city_title.append('<br />%d walls' % (len(the_city.walls)-1))
				else:
					city_title.append('<br />%d walls' % len(the_city.walls))
			else:
				if not has_harbour_walls:
					city_title.append('<br />1 wall')
			team_logo = '%s_walled.png' % team_clean_name
		
		# Supply
		if the_city.supplies != []:
			supply_string = ", ".join([resource_list.data_list[s].name for s in the_city.supplies])
			city_title.append('<br />%s' % supply_string)
		
		# Terrain
		city_title.append('<br />Terrain type: %s' % map_data.terrain[mapper_q.get_terrain(cursor, city_x, city_y)].title())
		
		# Area - Used for debugging overlap
		# area = image_size/2.5
		# area = area * area
		# city_title.append("<br />Area: %s" % area)
		
		# Overlap
		if the_city.overlap > 0:
			city_title.append('<br />Overlap: %s%%' % the_city.overlap)
		
		# Population
		if the_city.team not in self.personalise:
			city_title.append('<br />Size: %s' % common.approx(the_city.size))
			if the_city.slaves > 0:
				city_title.append('<br />Slaves: %s' % common.approx(the_city.slaves))
		else:
			city_title.append('<br />Population: %s' % common.number_format(the_city.population))
			if the_city.slaves > 0:
				city_title.append('<br />Slaves: %s' % common.number_format(the_city.slaves))
		
		# Artefact
		artefact_count = 0
		if city_id in self.cities_with_artefact:
			for a, the_artefact in self.artefact_dict.items():
				if the_artefact.city == city_id:
					artefact_count += 1
					
		if artefact_count > 0:
			city_is_special = True
			if artefact_count > 1:
				city_title.append('<br /><strong>City contains %d artefacts</strong>' % artefact_count)
			else:
				city_title.append('<br /><strong>City contains an artefact</strong>')
		
		# Wonder
		if city_id in self.cities_with_wonder:
			for w, the_wonder in self.wonder_dict.items():
				if the_wonder.city == city_id:
					if the_wonder.completed:
						city_title.append('<br /><strong>City contains a wonder</strong>')
						city_is_special = True
					else:
						city_title.append('<br /><strong>City contains an uncompleted wonder</strong>')
		
		# Description
		if the_city.description != '':
			city_title.append('<br />%s' % the_city.description.replace("\\", ""))
		
		# GM stuff
		if self.gm:
			city_title.append('<br />Image size: %s' % image_size)
		
		# Info only for the team map
		if the_city.team in self.personalise:
			city_title.append("<br />")
			
			# Buildings?
			# in_progress_dict, city_buildings = the_city.get_buildings()
			
			walls		= []
			buildings	= []
			in_progress = []
			
			for b, a in the_city.buildings_amount.items():
				if self.building_dict[b].wall == True: walls.append(self.building_dict[b].name)
				if self.building_dict[b].wall != True: buildings.append(self.building_dict[b].name)
			
			for b, p in the_city.buildings.items():
				if p > 0:
					in_progress.append(self.building_dict[b].name)
			
			if len(buildings) > 0:
				city_title.append("<br /><strong>Buildings</strong>: %s" % ", ".join(buildings))
			
			if len(walls) > 0:
				city_title.append("<br /><strong>Walls</strong>: %s" % ", ".join(walls))
			
			if len(in_progress) > 0:
				city_title.append("<br /><strong>In progress</strong>: %s" % ", ".join(in_progress))
		
		if the_city.founded == common.current_turn():
			new_city_style = "border: 1px solid #FFA;"
			city_title.append("<br />Founded: <strong>Turn %d</strong>" % the_city.founded)
		elif city_is_special:
			# new_city_style = "border: 2px dotted #FFF;"
			new_city_style = ""
			team_logo = '%s_special.png' % team_clean_name
		else:
			new_city_style = ""
			city_title.append("<br />Founded: Turn %d" % the_city.founded)
		
		# Land controlled?
		# control = ""
		# if the_city.team in self.personalise:
		# 	control_image_size = map_control_size(the_city.size)
		# 	if control_image_size == 0:
		# 		return ""
		# 	
		# 	c_left		= (the_city.x - self.left) * 2.5 - (control_image_size/2.0)
		# 	c_top		= (the_city.y - self.top) * 2.5 - (control_image_size/2.0)
		# 	
		# 	control = """<img class="city_icon" src="%(icon_path)scontrol.png" style="top:%(top)spx; left: %(left)spx;" width="%(image_size)s" height="%(image_size)s" />""" % {
		# 		"icon_path":	self.icon_path,
		# 		"top":			c_top,
		# 		"left":			c_left,
		# 		"image_size":	control_image_size,
		# 	}
		
		# # Output - Function float
		# output = """<img class="city_icon" id="{0[clean_name]}" src="{0[icon_path]}{0[team_logo]}" style="top:{0[top]}px; left:{0[left]}px;" width="{0[image_size]}" height="{0[image_size]}" onmouseover="$('#{0[clean_name]}_hover').fadeIn(250);" onmouseout="$('#{0[clean_name]}_hover').hide(250);"/>""".format({
		# 	"icon_path":	self.icon_path,
		# 	"clean_name":	clean_name,
		# 	"top": my_top,
		# 	"left": my_left,
		# 	"image_size": image_size,
		# 	"team_logo": team_logo,
		# })
		
		# Output - Fixed float
		output = """<img class="city_icon" id="{clean_name}" src="{icon_path}{team_logo}" style="top:{top}px; left:{left}px;{new_city}" width="{image_size}" height="{image_size}" onmouseover="$('#{clean_name}_hover').fadeIn(250);" onmouseout="$('#{clean_name}_hover').hide(250);"/>""".format(
			icon_path =		self.icon_path,
			clean_name =	clean_name,
			top =			my_top,
			left =			my_left,
			image_size =	image_size,
			team_logo =		team_logo,
			new_city =		new_city_style,
		)
		
		if self.mouseover == 1:
			hover_top = my_top - 5
			hover_top = min(self.height*2.5 - 125, hover_top)
			
			hover_left = my_left + image_size + 20
			hover_left = max(hover_left, 5)
		
			if hover_left > ((self.width * 2.5) - 350):
				hover_left = my_left - 350
		
			# Floater
			self.append_last.append("""<div id="%(clean_name)s_hover" class="city_hover" style="top:%(hover_top)spx; left:%(hover_left)spx;"><div class="city_title">%(name)s&nbsp;&nbsp;&nbsp;%(city_x)s,%(city_y)s</div>%(city_title)s</div>""" % {
				"name": the_city.name,
				"clean_name": clean_name,
				"hover_top": hover_top,
				"hover_left": hover_left,
				"city_x": the_city.x,
				"city_y": the_city.y,
				"city_title": "".join(city_title),
			})
		
		# Now return it
		return "".join(output)
	



CSS = """<style type="text/css" media="screen">
body
{
	background-color:		#FFF;
	color:					#222;
	
	padding:				0px;
	margin:					0px;
	
	font-family:			Helvetica, Arial, Verdana, sans-serif;
	font-size:				0.9em;
	line-height:			1.3em;
}

.theMap
{
	width:					{W}px;
	height:					{H}px;
	background-image:		url('{P}');
	background-repeat:		no-repeat;
	background-position:	{ML}px {MR}px;
}

.city_icon, .army_icon
{
	position:				absolute;
}

.city_hover, .army_hover
{
	background-image:		url('{T}');
	background-repeat:		repeat;
	position:				absolute;
	width:					320px;
	border:					1px solid #777;
	border:					none;
	padding:				3px;
	display:				none;
}

.city_title, .army_title
{
	text-align:			center;
	font-weight:		bold;
	margin:				-3px 20px 3px;
	border-bottom:		1px dotted #444;
	font-size:			1.2em;
	padding:			3px;
}

.edit_box
{
	position:absolute;
	cursor:pointer;
	text-align:center;
	color:#FFF;
}

.c_box
{
	position:absolute;
}

.colour_box
{
	position:absolute;
	cursor:pointer;
	text-align:center;
	color:#FFF;
	background-color: #AAA;
}
</style>"""

def map_source(source_dict, zoom=1):
	zoom = float(zoom)
	
	# Default map dimensions
	source_dict['mapper_css']	= source_dict.get("mapper_css", CSS)
	
	source_dict['left']			= source_dict.get("left", map_data.dimensions['left']*2.5*zoom)
	source_dict['right']		= source_dict.get("right", map_data.dimensions['right']*2.5*zoom)
	source_dict['top']			= source_dict.get("top", map_data.dimensions['top']*2.5*zoom)
	source_dict['bottom']		= source_dict.get("bottom", map_data.dimensions['bottom']*2.5*zoom)
	
	source_dict['margin_left']	= source_dict.get("margin_left", map_data.dimensions['margin_left']*2.5*zoom)
	source_dict['margin_top']	= source_dict.get("margin_top", map_data.dimensions['margin_top']*2.5*zoom)
	
	source_dict['map_width']	= source_dict.get("map_width", (source_dict['right'] - source_dict['left']))
	source_dict['map_height']	= source_dict.get("map_height", (source_dict['bottom'] - source_dict['top']))
	
	source_dict['title']		= source_dict.get("title", "World of Arl Map")
	
	# Paths
	if source_dict.get("build", 0) == 1:
		source_dict['map_path']			= source_dict.get("map_path", "images/theMap.jpg")
		source_dict['jquery']			= source_dict.get("jquery", "../includes/jquery.js")
		source_dict['transparent_path']	= source_dict.get("transparent_path", "images/trans75.png")
		source_dict['key_path']			= source_dict.get("key_path", "images/key.png")
		source_dict['analytics']		= source_dict.get("analytics", common.data['analytics'])

	else:
		# source_dict['map_path']			= source_dict.get("map_path", "http://localhost/WoA/map/images/theMap.jpg")
		source_dict['map_path']			= source_dict.get("map_path", "http://localhost/WoA/map/images/theMap.jpg")
		source_dict['jquery']			= source_dict.get("jquery", "%s%s" % (common.data['media_path'], "jquery.js"))
		source_dict['transparent_path']	= source_dict.get("transparent_path", "http://localhost/WoA/map/images/trans75.png")
		source_dict['key_path']			= source_dict.get("key_path", "http://localhost/WoA/map/images/key.png")
		source_dict['analytics']		= source_dict.get("analytics", '')
	
	# source_dict['output'] = ''
	# source_dict['analytics'] = ''
	# source_dict['mapper_css'] = ''
	# for k, v in source_dict.items():
	# 	print k, ": ", v
	
	# Onclick stuff
	source_dict["new_mode"]				= source_dict.get("new_mode", "")
	source_dict["new_mode_form_fields"]	= source_dict.get("new_mode_form_fields", "")
	source_dict["map_click_handler"]	= source_dict.get("map_click_handler", "alert(alert_string);")
	source_dict["onclick_js"]			= source_dict.get("onclick_js", """
	var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
	var map_y = parseInt(document.getElementById('labelHideY').innerHTML);
	
	use_map_xy(map_x, map_y);""")
	
	source_dict["header"]				= source_dict.get("header", "")
	source_dict["footer"]				= source_dict.get("footer", "")
	
	# Legend, do we include it?
	source_dict['map_legend']	= source_dict.get("map_legend", """
	<div style="position:absolute;background-image:url('%(transparent_path)s');padding:5px;width:350px;">
		<form action="#" onsubmit="window.location='http://woarl.com/map/turn_' + $('#turn').val() + '_normal.html'; return false;" method="get" accept-charset="utf-8">
			<input type="submit" value="Show map for turn:" />
			<input type="text" name="turn" id="turn" value="" size="5" />
		</form>
	<div id="map_legend">
		<br />
		<strong style="font-size:1.2em;">Legend</strong>
		
		<a href="#" id="map_key_show" style="float:right;padding-right:20px;" onclick="$('#map_key_img').show(1000); $('#map_key_show').hide(); return false;">Show legend</a>
		<!--<a href="#" style="float:right;padding-right:20px;" onclick="$('#map_legend').hide(1000); return false;">Hide</a>-->
		 - 
		<a href="%(map_path)s" style="float:right;padding-right:20px;">No icons</a>
		<br />
		<img style="display:none;" id="map_key_img" src="%(key_path)s"/>
	</div>
	</div>""" % source_dict)
	
	return """
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
			"http://www.w3.org/TR/html4/loose.dtd">
	<html>
		<head>
			<title>%(title)s</title>
			<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
			<script src="%(jquery)s" type="text/javascript" charset="utf-8"></script>
			<style type="text/css" media="screen">
				body
				{
					background-color:		#FFF;
					color:					#222;

					padding:				0px;
					margin:					0px;

					font-family:			Helvetica, Arial, Verdana, sans-serif;
					font-size:				0.9em;
					line-height:			1.3em;
				}

				.theMap
				{
					width:					%(map_width)spx;
					height:					%(map_height)spx;
					background-image:		url('%(map_path)s');
					background-repeat:		no-repeat;
					background-position:	%(margin_left)spx %(margin_top)spx;
				}

				.city_icon, .army_icon
				{
					position:				absolute;
				}

				.city_hover, .army_hover
				{
					background-image:		url('%(transparent_path)s');
					background-repeat:		repeat;
					position:				absolute;
					width:					320px;
					border:					1px solid #777;
					border:					none;
					padding:				3px;
					display:				none;
				}

				.city_title, .army_title
				{
					text-align:			center;
					font-weight:		bold;
					margin:				-3px 20px 3px;
					border-bottom:		1px dotted #444;
					font-size:			1.2em;
					padding:			3px;
				}

				.edit_box
				{
					position:absolute;
					cursor:pointer;
					text-align:center;
					color:#FFF;
				}
				
				.c_box
				{
					position:absolute;
				}

				.colour_box
				{
					position:absolute;
					cursor:pointer;
					text-align:center;
					color:#FFF;
					background-color: #AAA;
				}
			</style>
			
			<script type='text/javascript' charset='utf-8'>
				var IE = document.all ? true : false;

				if (!IE)
				{
					document.captureEvents(Event.MOUSEMOVE)
					// document.captureEvents(Event.MOUSECLICK)
				}

				document.onmousemove = get_mouse_xy;
				// document.onmouseclick = get_mouse_xy;
				var temp_x = 0;
				var temp_y = 0;

				function get_mouse_xy(e)
				{
					if (IE)
					{
						// grab the x-y pos.s if browser is IE
						temp_x = event.clientX + (document.documentElement.scrollLeft || document.body.scrollLeft);
						temp_y = event.clientY + (document.documentElement.scrollTop || document.body.scrollTop);
					}
					else
					{
						// grab the x-y pos.s if browser is Not IE
						temp_x = e.pageX;
						temp_y = e.pageY;
					}  

					// if (temp_x < 0){temp_x = 0;}
					if (temp_y < 0){temp_y = 0;}

					document.getElementById('labelHideX').innerHTML = temp_x
					document.getElementById('labelHideY').innerHTML = temp_y;
					return true;
				}

				function use_map_xy(map_x, map_y)
				{
					// Do stuff!
					var actualX, actualY;
					
					var alert_string = '';
					
					if (IE)
					{
						actualX = map_x;
						actualY = map_y;

						actualX = Math.round(actualX/2.5);
						actualY = Math.round(actualY/2.5);

						actualX = actualX + (%(left)s/2.5);
						actualY = actualY + (%(top)s/2.5);
						
						alert_string += '' + actualX + ', ' + actualY;
					}
					else
					{
						// actualX = Math.round(map_x/2.5) + %(left)s;
						// actualY = Math.round(map_y/2.5) + %(top)s;
						
						// alert_string += actualX + ', ' + actualY;
						
						actualX = map_x;
						actualY = map_y;
						
						actualX = Math.round(actualX/2.5);
						actualY = Math.round(actualY/2.5);
						
						actualX = actualX + (%(left)s/2.5);
						actualY = actualY + (%(top)s/2.5);
						
						alert_string += '' + parseInt(actualX) + ', ' + parseInt(actualY);
					}

					//$('#location').val(alert_string);
					%(map_click_handler)s
				}

				function find_pos_x(obj)
				{
					var curleft = 0;
					if(obj.offsetParent)
					{
						while(1) 
						{
							curleft += obj.offsetLeft;
							if(!obj.offsetParent)
							{
								break;
							}
							obj = obj.offsetParent;
						}
					}
					else if(obj.x)
					{
						curleft += obj.x;
					}
					return curleft;
				}

				function find_pos_y(obj)
				{
					var curtop = 0;
					if(obj.offsetParent)
					{
						while(1)
						{
							curtop += obj.offsetTop;
							if(!obj.offsetParent)
							{
								break;
							}
							obj = obj.offsetParent;
						}
					}
					else if(obj.y)
					{
						curtop += obj.y;
					}

					return curtop;
				}
			</script>
		</head>
		<body onload="var loc = String(document.location); loc = loc.split('#'); loc = '#' + loc[1]; loc = loc.replace('mv_', '');
		$('html, body').animate({scrollTop: $(loc).offset().top-($(window).height()/2)}, 0); $('html, body').animate({scrollLeft: $(loc).offset().left-($(window).width()/2)}, 0);
		">
			<span style="display:none;" id="labelHideXIE"></span>
			<span style="display:none;" id="labelHideYIE"></span>

			<span style="display:none;" id="labelHideX"></span>
			<span style="display:none;" id="labelHideY"></span>

			<form action="web.py" style="display:none;" id="new_mode_form" method="post">
				<input type="hidden" name="mode" value="%(new_mode)s" />
				<input type="hidden" name="location" id="location" value="" />
				%(new_mode_form_fields)s
			</form>
			%(map_legend)s
			<div class="theMap" onclick="%(onclick_js)s">
				%(header)s
				%(output)s
				%(footer)s
			</div>
			%(analytics)s
		</body>
	</html>""" % source_dict
