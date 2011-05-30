import json
from classes import mapper
from queries import mapper_q
from functions import path_f
from rules import map_data, map_resources
from lists import resource_list
from pages import common

class JSON_map_maker (mapper.Map_maker):
	# def map_grid(self, cursor):
	# 	self._setup_grid(cursor)
	# 	output = self._map_grid(cursor)
	# 	return output
	
	def _map_grid(self, cursor):
		cities = {}
		armies = {}
		stats = {}
		
		# Map stats
		stats['left']	= map_data.dimensions['left']
		stats['right']	= map_data.dimensions['right']
		stats['top']	= map_data.dimensions['top']
		stats['bottom']	= map_data.dimensions['bottom']
		
		# Cities
		for c in self.city_dict.keys():
			cities[c] = self.draw_city(cursor, c)
		
		# Armies
		if self.draw_armies == True or len(self.personalise):
			self.army_dict = army_q.get_all_non_garrisons(cursor)
			
			for a in self.army_dict.keys():
				if self.draw_armies or self.army_dict[a].team in self.personalise:
					self.army_dict[a].get_size(cursor)
					armies[a] = self.draw_army(a)
		
		return json.dumps({
			"armies": armies,
			"cities": cities,
			"stats": stats,
		})
	
	def draw_city(self, cursor, city_id):
		city_is_special = False
		
		# Handles
		the_city = self.city_dict[city_id]
		the_team = self.team_dict[the_city.team]
		
		# Test for 1 icon
		image_size = map_data.map_image_size(the_city.size)
		
		# Check it's within the picture size of the map
		if (the_city.x - image_size/2) < self.left:		return
		if (the_city.x + image_size/2) > self.right:	return
		
		if (the_city.y - image_size/2) < self.top:		return
		if (the_city.y + image_size/2) > self.bottom:	return
		
		output = {}
		
		# System type stuff
		output['pixel_x'] = (the_city.x - self.left) * 2.5 - (image_size/2.0)
		output['pixel_y'] = (the_city.y - self.top) * 2.5 - (image_size/2.0)
		
		# Owner
		output['team.id'] = the_team.id
		output['team.name'] = the_team.name
		
		# Key stats
		output['id'] = the_city.id
		output['name'] = the_city.name
		output['x'] = the_city.x
		output['y'] = the_city.y
		output['port'] = the_city.port
		output['nomadic'] = the_city.nomadic
		output['founded'] = the_city.founded
		
		# Walls
		output['harbour_walls'] = False
		if 18 in the_city.buildings_amount and the_city.buildings_amount[18] > 0:# Harbour walls id = 18
			output['harbour_walls'] = True
		
		output['wall_count'] = 0
		if the_city.walls != []:
			if len(the_city.walls) > 1:
				if output['harbour_walls']:
					output['wall_count'] = len(the_city.walls) - 1
				else:
					output['wall_count'] = len(the_city.walls)
			elif not output['harbour_walls']:
				output['wall_count'] = len(the_city.walls)
		
		# Supplies and Terrain
		output['supplies'] = the_city.supplies
		output['terrain'] = map_data.terrain[mapper_q.get_terrain(cursor, the_city.x, the_city.y)].title()
		
		city_loc = (the_city.x - (the_city.x % 10), the_city.y - (the_city.y % 10))
		output['continent'] = path_f.get_map_continent_tiles(cursor).get(city_loc, -1)
		
		# Overlap
		output['supplies'] = the_city.overlap
		
		# Population
		if the_city.team not in self.personalise:
			output['size'] = common.napprox(the_city.size)
			output['slaves'] = common.napprox(the_city.slaves)
			
		else:
			output['size'] = the_city.size
			output['population'] = the_city.population
			output['slaves'] = the_city.slaves
		
		# Artefact
		artefact_count = 0
		if city_id in self.cities_with_artefact:
			for a, the_artefact in self.artefact_dict.items():
				if the_artefact.city == city_id:
					artefact_count += 1
		
		output['artefacts'] = artefact_count
		
		# Wonder
		output['wonder'] = "None"
		if city_id in self.cities_with_wonder:
			for w, the_wonder in self.wonder_dict.items():
				if the_wonder.city == city_id:
					if the_wonder.completed:
						output['wonder'] = "Complete"
					else:
						output['wonder'] = "Incomplete"
		
		# Description
		output['description'] = the_city.description
		
		# # Info only for the team map
		# if the_city.team in self.personalise:
		# 	walls		= []
		# 	buildings	= []
		# 	in_progress = []
		# 	
		# 	for b, a in the_city.buildings_amount.items():
		# 		if self.building_dict[b].wall == True: walls.append(self.building_dict[b].name)
		# 		if self.building_dict[b].wall != True: buildings.append(self.building_dict[b].name)
		# 	
		# 	for b, p in the_city.buildings.items():
		# 		if p > 0:
		# 			in_progress.append(self.building_dict[b].name)
		# 	
		# 	if len(buildings) > 0:
		# 		city_title.append("<br /><strong>Buildings</strong>: %s" % ", ".join(buildings))
		# 	
		# 	if len(walls) > 0:
		# 		city_title.append("<br /><strong>Walls</strong>: %s" % ", ".join(walls))
		# 	
		# 	if len(in_progress) > 0:
		# 		city_title.append("<br /><strong>In progress</strong>: %s" % ", ".join(in_progress))
		
		# Now return it
		return output
	
	def draw_army(self, army_id):
		output = {}
		
		the_army = self.army_dict[army_id]
		the_team = self.team_dict[the_army.team]
		
		if the_army.size < 1:
			return
		
		# Test for 1 icon
		image_size = 40
		output['pixel_x'] = (the_army.x - self.left) * 2.5 - (image_size/2)
		output['pixel_y'] = (the_army.y - self.top) * 2.5 - (image_size/2)
		
		#	Mouseover
		#------------------------
		# Owner
		output['team.id'] = the_team.id
		output['team.name'] = the_team.name
		
		# Stats
		output['id'] = the_army.id
		output['name'] = the_army.name
		output['x'] = the_army.x
		output['y'] = the_army.y
		output['size'] = the_army.size
		
		return output