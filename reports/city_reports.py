from pages import common
from queries import city_q, mapper_q
from functions import city_f, path_f
from rules import map_data

def water_cities(cursor):
	sea = []
	lakes = []
	
	city_dict = city_q.get_live_cities(cursor)
	for k, c in city_dict.items():
		t = mapper_q.get_terrain(cursor, c.x, c.y)
		
		if t == 0:
			sea.append("%s (%d)" % (c.name, k))
		if t == map_data.terrain.index("lake"):
			lakes.append("%s (%d)" % (c.name, k))
	
	if sea != []:
		sea.insert(0, "[r]Sea based cities[/r]")
		sea.append("\n")
	
	if lakes != []:
		lakes.insert(0, "[r]Lake based cities[/r]")
		lakes.append("\n")
	
	return "%s%s" % ("\n".join(sea), "\n".join(lakes))

def port_cities(cursor):
	output = []
	
	city_dict = city_q.get_live_cities(cursor)
	for k, c in city_dict.items():
		if not c.port: continue
		
		landlocked = True
		
		if landlocked and mapper_q.get_terrain(cursor, c.x - 10, c.y - 10) == 0: landlocked = False
		if landlocked and mapper_q.get_terrain(cursor, c.x, c.y - 10) == 0: landlocked = False
		if landlocked and mapper_q.get_terrain(cursor, c.x + 10, c.y - 10) == 0: landlocked = False
		
		if landlocked and mapper_q.get_terrain(cursor, c.x - 10, c.y) == 0: landlocked = False
		if landlocked and mapper_q.get_terrain(cursor, c.x + 10, c.y) == 0: landlocked = False
		
		if landlocked and mapper_q.get_terrain(cursor, c.x - 10, c.y + 10) == 0: landlocked = False
		if landlocked and mapper_q.get_terrain(cursor, c.x, c.y + 10) == 0: landlocked = False
		if landlocked and mapper_q.get_terrain(cursor, c.x + 10, c.y + 10) == 0: landlocked = False
		
		if landlocked:
			output.append("%s (%d)" % (c.name, k))
	
	if output != []:
		output.insert(0, "[r]Landlocked ports[/r]")
		output.append("\n")
	
	return "\n".join(output)

def run(cursor, verbose):
	output = []
	
	output.append(water_cities(cursor))
	output.append(port_cities(cursor))
	
	return "".join(output)