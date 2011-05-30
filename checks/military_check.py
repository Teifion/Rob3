import database
from functions import unit_f, army_f, path_f, cli_f
from queries import unit_q, mapper_q, equipment_q, team_q, army_q, city_q, mapper_q
from classes import world, unit, team
from data_classes import equipment
from rules import map_data

def check_army_bases(cursor, verbose):
	team_dict = team_q.get_all_teams(cursor)
	army_dict = army_q.get_armies_from_team_list(cursor, list(team_dict.keys()))
	city_dict = city_q.get_live_cities(cursor)
	relations = team_q.get_relations(cursor)# [Host][Visitor]
	
	# Build up a shortlist dict of cities by team
	city_by_team = {}
	for team_id, the_team in team_dict.items():
		if team_id not in city_by_team:
			city_by_team[team_id] = []
		
		for city_id, the_city in city_dict.items():
			if the_city.team == team_id or relations.get(the_city.team, {}).get(team_id, {}).get('border', team_dict[the_city.team].default_borders) >= team.border_states.index("Allied"):
				city_by_team[team_id].append(city_id)
	
	# Now to run through the armies and find their paths
	new_bases = set()
	# for i in progressbar(range(15), "Computing: ", 40):
	# for army_id, the_army in army_dict.items():
	
	if verbose:
		it = cli_f.progressbar(army_dict.items(), "military_check.check_army_bases: ", 40, with_eta = True)
	else:
		it = army_dict.items()
	
	for army_id, the_army in it:
		army_terrain = mapper_q.get_terrain(cursor, the_army.x, the_army.y)
		
		for city_id in city_by_team[the_army.team]:
			if army_terrain < 1:
				if not the_city.port: continue
			
			the_city = city_dict[city_id]
			if the_city.dead > 0: continue
			dist = path_f.pythagoras((the_army.x, the_army.y), (the_city.x, the_city.y))
			
			if dist < 10:
				the_army.base = city_id
				the_army.distance = (dist/map_data.movement_speeds['Marching'])*10# Distance over speed in km, 1 distance unit is 10k
				new_bases.add(army_id)
			
		# Extend the search a little
		if army_id not in new_bases:
			for city_id in city_by_team[the_army.team]:
				if army_terrain < 1:
					if not the_city.port: continue
				
				the_city = city_dict[city_id]
				dist = path_f.pythagoras((the_army.x, the_army.y), (the_city.x, the_city.y))
			
				if dist < 30:
					the_army.base = city_id
					the_army.distance = (dist/map_data.movement_speeds['Marching'])*10# Distance over speed in km, 1 distance unit is 10k
					new_bases.add(army_id)
		
		# Extend the search a little
		if army_id not in new_bases:
			for city_id in city_by_team[the_army.team]:
				if army_terrain < 1:
					if not the_city.port: continue
				
				the_city = city_dict[city_id]
				dist = path_f.pythagoras((the_army.x, the_army.y), (the_city.x, the_city.y))
			
				if dist < 60:
					the_army.base = city_id
					the_army.distance = (dist/map_data.movement_speeds['Marching'])*10# Distance over speed in km, 1 distance unit is 10k
					new_bases.add(army_id)
		
		# If we can't find an easy solution we start pathing
		if army_id not in new_bases:
			fastest_path = (-1, 9999999)
			
			for city_id in city_by_team[the_army.team]:
				the_city = city_dict[city_id]
				
				# Small cities won't support an army a long way away right?
				if the_city.size < 5000: continue
				
				# Is it a fleet?
				if army_terrain < 1:
					if not the_city.port: continue
					
					# Now lets try water
					dist = path_f.path(cursor, ((the_army.x, the_army.y), (the_city.x, the_city.y)), move_speed="Sailing", move_type="Sail")
					
					if dist.time_cost < fastest_path[1]:
						fastest_path = (city_id, dist.time_cost)
				
				else:
					# I'm sure there's a way to improve this...
					dist = path_f.path(cursor, ((the_army.x, the_army.y), (the_city.x, the_city.y)), move_speed="Marching", move_type="Medium foot")
					
					if dist.time_cost == 0:
						continue
					
					# if army_id == 960 and city_id == 1098:
					# 	print("")
					# 	print(dir(dist))
					# 	print(((the_army.x, the_army.y), (the_city.x, the_city.y)))
					# 	print(dist.time_cost)
					# 	print(dist.walk_distance)
					# 	print(len(dist.steps))
					# 	print("")
					
					if dist.time_cost < fastest_path[1]:
						fastest_path = (city_id, dist.time_cost)
				
			the_army.base = fastest_path[0]
			the_army.distance = fastest_path[1]
			new_bases.add(army_id)
	
	# Reset all armies
	query = """UPDATE armies SET base = -1, distance = -1 WHERE garrison = 0;"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for a in new_bases:
		query = """UPDATE armies SET base = %d, distance = %d WHERE id = %d;""" % (army_dict[a].base, army_dict[a].distance, a)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Garrisons automatically go to their city
	query = """UPDATE armies SET base = garrison, distance = 0 WHERE garrison > 0;"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

def build_unit_equipment_strings(cursor, verbose):
	# Does what it says on the tin
	the_world = world.World(cursor)
	# the_world.units()
	unit_dict = unit_q.get_all_live_units(cursor)
	
	if verbose:
		it = cli_f.progressbar(unit_dict.items(), "military_check.build_unit_equipment_strings: ", 40, with_eta = True)
	else:
		it = unit_dict.items()
	
	for unit_id, the_unit in it:
		unit_f.rebuild_equipment_string(cursor, unit_id, the_world)


def check_for_garrisons(cursor, verbose):
	garrisons_made = 0
	garrisons_named = 0
	
	city_list = []
	city_names = {}
	garrison_names = {}
	# Get cities
	query = "SELECT id, name FROM cities WHERE dead < 1"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		city_list.append(row['id'])
		city_names[row['id']] = row['name']
	
	# Get garrisons
	query = "SELECT garrison, name FROM armies WHERE garrison > 0;"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		garrison_names[row['garrison']] = row['name']
	
	if verbose:
		it = cli_f.progressbar(city_list, "military_check.check_for_garrisons: ", 40, with_eta = True)
	else:
		it = city_list
	
	for city_id in it:
		# row = cursor.fetchone()
		if city_id not in garrison_names:
			# No garrison exists for this city, best create one
			database.query(cursor, army_f.create_garrison(cursor, city_id))
			garrisons_made += 1
		else:
			# Has a garrison, lets check the name
			if garrison_names[city_id] != "%s garrison" % city_names[city_id]:
				database.query(cursor, army_f.name_garrison(city_id, city_names[city_id]))
				garrisons_named += 1
			


def remove_garrisons(cursor, verbose):
	"""Removes garrisons and armies from teams that are not active"""
	team_list = []
	query = """SELECT id FROM teams WHERE active = False"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		team_list.append(str(row['id']))
	
	team_list = ",".join(team_list)
	
	army_list = []
	query = """SELECT id FROM armies WHERE team IN (%s)""" % team_list
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		army_list.append(str(row['id']))
	army_list = ",".join(army_list)
	
	# Now to find garrisons without a city
	city_list = []
	query = "SELECT id FROM cities"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		city_list.append(row['id'])
	
	query = """SELECT id, garrison FROM armies WHERE garrison > 0"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['garrison'] not in city_list:
			if row['id'] not in army_list:
				army_list.append(row['id'])
	
	# Delete stuff
	query = """DELETE FROM armies WHERE id IN (%s)""" % army_list
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	query = """DELETE FROM squads WHERE army IN (%s)""" % army_list
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if verbose:
		print("military_check.remove_garrisons() removed all garrisons missing a city")


def check_unit_categories(cursor, verbose):
	queries = []
	unit_dict = unit_q.get_all_live_units(cursor)
	equipment_dict = equipment_q.get_all_equipment(cursor)
	
	unit_q.mass_get_unit_equipment(cursor, unit_dict)
	
	# Default
	query = """UPDATE units SET crew = 1;"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if verbose:
		it = cli_f.progressbar(unit_dict.items(), "military_check.check_unit_categories: ", 40, with_eta = True)
	else:
		it = unit_dict.items()
	
	for unit_id, the_unit in it:
		the_unit.transport = 0
		the_unit.move_type = 0
		the_unit.move_speed = 0
		the_unit.crew = 1
		
		the_unit.weapon_cat = 0
		the_unit.armour_cat = 0
		the_unit.move_cat = 0
		the_unit.training_cat = 0
		
		ranged = False
		melee = False
		
		# Loop through all it's equipment
		for e in the_unit.equipment:
			the_e = equipment_dict[e]
			
			if the_e.range > 2:
				ranged = True
			elif the_e.range == 0:
				melee = True
			
			the_unit.transport = max(the_e.transport, the_unit.transport)
			
			the_unit.crew = max(the_unit.crew, the_e.crew)
			
			# the_unit.move_type = 0
			# the_unit.move_speed = 0
			# the_unit.type_cat = 0
			
			the_unit.armour_cat = max(the_unit.armour_cat, the_e.armour_cat)
			the_unit.move_cat = max(the_unit.move_cat, the_e.move_cat)
			the_unit.training_cat = max(the_unit.training_cat, the_e.training_cat)
			
			if the_e.category == equipment.cat_list.index("Boat hull"):
				the_unit.type_cat = unit.categories.index("Ship")
			elif the_e.category == equipment.cat_list.index("Balloon"):
				the_unit.type_cat = unit.categories.index("Airship")
			else:
				pass
		
		# Work out categories
		if ranged and melee:
			the_unit.weapon_cat = unit.weapon_categories.index("Melee and Ranged")
		elif ranged and not melee:
			the_unit.weapon_cat = unit.weapon_categories.index("Ranged")
		elif melee and not ranged:
			the_unit.weapon_cat = unit.weapon_categories.index("Melee")
		else:
			the_unit.weapon_cat = unit.weapon_categories.index("Neither")
		
		# Query
		queries.append("""UPDATE units SET
			transport = {transport}, move_type = {move_type}, move_speed = {move_speed}, crew = {crew},
			type_cat = {type_cat}, weapon_cat = {weapon_cat}, armour_cat = {armour_cat}, move_cat = {move_cat}, training_cat = {training_cat}
				WHERE id = {id};""".format(
			transport = the_unit.transport,
			move_type = the_unit.move_type,
			move_speed = the_unit.move_speed,
			crew = the_unit.crew,
			type_cat = the_unit.type_cat,
			weapon_cat = the_unit.weapon_cat,
			armour_cat = the_unit.armour_cat,
			move_cat = the_unit.move_cat,
			training_cat = the_unit.training_cat,
			id = the_unit.id,
		))
	
	database.query(cursor, queries)


def delete_empty_squads_from_dead_garrisons(cursor, verbose):
	return
	
	# Get list of armies that are "dead"
	dead_list = []
	query = "SELECT a.id FROM cities c, armies a WHERE c.dead = True AND c.id = a.garrison"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		dead_list.append(str(row['id']))
	
	# Get list of squads we can delete
	query = "DELETE FROM squads WHERE army in (%s) AND amount < 1" % ",".join(dead_list)
	dead_list = []
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		dead_list.append(str(row['id']))
	
	# Now to delete battle history
	exit("miltary_check.delete_empty_squads_from_dead_garrisons()")


class Team_lands (object):
	"""docstring for Team_lands"""
	def __init__(self, team_id):
		super(Team_lands, self).__init__()
		self.id = team_id
		
		self.continents 	= []
		self.terrain		= []
		self.land_matrix	= {}
	
	def add_city(self, continent, terrain):
		# Lists
		if continent not in self.continents: self.continents.append(continent)
		if terrain not in self.terrain: self.terrain.append(terrain)
		
		# Matrix
		if continent not in self.land_matrix: self.land_matrix[continent] = []
		if terrain not in self.land_matrix[continent]: self.land_matrix[continent].append(terrain)
	
	def check_matrix(self, continent, terrain):
		# Essentially a simple way to perform a 2D array search
		if continent not in self.land_matrix: return False
		if terrain not in self.land_matrix[continent]: return False
		
		return True


def check_available(cursor, verbose):
	the_world = world.World(cursor)
	
	unit_dict				= the_world.units()
	unit_q.mass_get_unit_equipment(cursor, the_world._units)
	
	equipment_dict			= the_world.equipment()
	city_dict				= the_world.cities()
	terrain_tuples			= mapper_q.get_all_terrain(cursor)
	map_continent_tiles		= path_f.get_map_continent_tiles(cursor)
	
	# First we need to get the continents and terrains of each team
	team_dict = {}
	
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "military_check.check_available: ", 40, with_eta = True)
	else:
		it = city_dict.items()
	
	for city_id, the_city in it:
		if the_city.dead > 0: continue
		if the_city.team not in team_dict: team_dict[the_city.team] = Team_lands(the_city.team)
		
		city_loc = (the_city.x - (the_city.x % 10), the_city.y - (the_city.y % 10))
		
		city_terrain, city_continent = 0, 0
		
		if city_loc in terrain_tuples: city_terrain = terrain_tuples[city_loc]
		if city_loc in map_continent_tiles: city_continent = map_continent_tiles[city_loc]
		
		team_dict[the_city.team].add_city(city_continent, city_terrain)
	
	# Next we'd get the techs too if possible
	
	
	# Now we go through each unit and find out if it's availiable
	not_available			= []
	for unit_id, the_unit in unit_dict.items():
		if the_unit.team < 2: continue# Skip units that are for all teams
		
		# If a team doesn't exist in the dictionary then it's because they've no cities
		if the_unit.team not in team_dict:
			# not_available.append(unit_id)
			continue
		
		checked_unit = False
		the_team = team_dict[the_unit.team]
		
		for e in the_unit.equipment:
			if checked_unit: continue
			the_equipment = equipment_dict[e]
			
			if the_equipment.continent > 0:
				if the_equipment.terrain > 0:
					# Need both
					if not the_team.check_matrix(the_equipment.continent, the_equipment.terrain):
						not_available.append(unit_id)
						checked_unit = True
				else:
					# Just continent
					if the_equipment.continent not in the_team.continents:
						not_available.append(unit_id)
						checked_unit = True
			else:
				if the_equipment.terrain > 0:
					# Just terrain
					if the_equipment.terrain not in the_team.terrain:
						not_available.append(unit_id)
						checked_unit = True
			
			# Now we can check tech level too
				
			# self.add_field("terrain",				"int")# 0 = Any terrain
			# self.add_field("tech",					"int")# 0 = No tech needed
			# self.add_field("tech_level",			"int")# 0 = No tech needed
	
	query = """UPDATE units SET available = True;"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if not_available != []:
		query = """UPDATE units
			SET available = False
				WHERE id IN (%s);""" % "".join([str(u) for u in not_available])
		
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

	
def merge_squads(cursor, verbose):
	the_world = world.World(cursor)
	
	squad_dict = the_world.squads()
	army_dict = the_world.armies()
	teams_dict = the_world.teams()
	
	squad_by_army = {}
	for k, s in squad_dict.items():
		if s.army not in squad_by_army: squad_by_army[s.army] = []
		squad_by_army[s.army].append(s.id)
	
	# Get active teams
	active_teams = []
	for team_id, the_team in teams_dict.items():
		if the_team.ir or not the_team.active: continue
		active_teams.append(team_id)
	
	# Pairs will contain tuples of what we want to merge
	queries = []
	
	if verbose:
		it = cli_f.progressbar(army_dict.items(), "military_check.merge_squads: ", 40, with_eta = True)
	else:
		it = army_dict.items()
	
	for army_id, the_army in it:
		if the_army.team not in active_teams: continue
		if army_id not in squad_by_army: continue
	
		skip_squads = []
	
		# Outside loop looks at the squad we may want to merge
		for squad_id_1 in squad_by_army[army_id]:
			if squad_id_1 in skip_squads: continue
		
			the_squad_1 = squad_dict[squad_id_1]
		
			for squad_id_2 in squad_by_army[army_id]:
				if squad_id_1 == squad_id_2: continue
				if squad_id_2 in skip_squads: continue
			
				the_squad_2 = squad_dict[squad_id_2]
			
				if the_squad_1.unit == the_squad_2.unit:
					if the_squad_1.name == the_squad_2.name:
						skip_squads.append(squad_id_2)
					
						# Update size
						queries.append("UPDATE squads SET amount = %d WHERE id = %d;" % (the_squad_1.amount + the_squad_2.amount, squad_id_1))
					
						# Delete 2nd squad
						queries.append("DELETE FROM squads WHERE id = %d" % squad_id_2)
	
	# print "\n".join(queries)
	cursor.execute("BEGIN")
	for query in queries:
		try: cursor.execute(query)
		except Exception as e:
			cursor.execute("ROLLBACK")
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	cursor.execute("COMMIT")		


def check_unit_ownership(cursor, verbose):
	team_dict = team_q.get_real_active_teams(cursor, skip_irs=False)
	
	# First we find the squads owned by a team that the army is not
	alert_list = []
	delete_list = []
	query = """SELECT s.id, s.team, s.amount
		FROM squads s, armies a
			WHERE s.army = a.id AND s.team != a.team"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['amount'] > 0:
			if row['team'] not in team_dict:
				delete_list.append(str(row['id']))
			else:
				alert_list.append(str(row['id']))
		else:
			delete_list.append(str(row['id']))
	
	if len(delete_list) > 0:
		query = """DELETE FROM squad_battle_history WHERE squad in (%s)""" % ",".join(delete_list)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		query = """DELETE FROM squads WHERE id in (%s)""" % ",".join(delete_list)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
			
		if verbose:
			print("military_check.check_unit_ownership deleted %d squads" % len(delete_list))
			
	
	if len(alert_list) > 0:
		print("Found squads that we can't delete")
		print(alert_list)


def run(cursor, check_all, verbose):
	check_unit_ownership(cursor, verbose)
	
	check_unit_categories(cursor, verbose)
	delete_empty_squads_from_dead_garrisons(cursor, verbose)
	build_unit_equipment_strings(cursor, verbose)
	check_for_garrisons(cursor, verbose)
	check_available(cursor, verbose)
	merge_squads(cursor, verbose)
	
	if check_all:
		check_army_bases(cursor, verbose)
	
	if verbose:
		print(database.shell_text("[g]Military checks complete[/g]"))