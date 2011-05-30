from pages import common
from queries import mapper_q
from lists import resource_list
from rules import map_data
import database

page_data = {
	"Title":	"Team list",
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	# Get the values
	x			= int(common.get_val('x', 0))
	y			= int(common.get_val('y', 0))
	grid_size	= int(common.get_val('grid', 0))
	new_terrain	= common.get_val('terrain', '')
	new_resource = common.get_val('resource', '')
	
	if new_terrain != '':
		terrain_index = map_data.terrain.index(new_terrain)
		
		# Get a list of all the tiles that will be affected
		tile_list = []
		
		for xx in range(x, x+grid_size, 10):
			for yy in range(y, y+grid_size, 10):
				tile_list.append((xx, yy))
		
		# Now to set ALL of these to that value
		mapper_q.set_terrain(cursor, tile_list, terrain_index)
		
		# Output
		if new_terrain == "water": new_terrain = ""
		
		if grid_size == 10:	return new_terrain[0:3]
		else:				return "<br />%s" % new_terrain
	
	elif new_resource != '':
		# Get the resource
		resource_index = resource_list.data_dict_n_l[new_resource.lower()]
		
		# Get a list of all the tiles that will be affected
		tile_list = []
		
		for xx in range(x, x+grid_size, 10):
			for yy in range(y, y+grid_size, 10):
				tile_list.append((xx, yy))
		
		# Now to set ALL of these to that value
		mapper_q.set_resource(cursor, tile_list, resource_index)
		
		if grid_size == 10:	return new_resource[0:3]
		else:				return "<br />%s" % new_resource
	
	else:
		return "No terrrain or resource"