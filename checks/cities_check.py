import database
from pages import common
from queries import city_q, building_q, mapper_q
from rules import map_resources
from rules import map_data, city_rules
from functions import path_f, city_f, cli_f, trade_f
from classes import world

def check_for_dead_cities(cursor, verbose):
	query = """UPDATE cities SET dead = %d WHERE population < 1 AND dead < 1;""" % common.current_turn()
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))


def check_for_amount(cursor, verbose):
	"""Takes all 100% buildings and makes them 0% but adds one to the amount"""
	building_dict = building_q.get_all_buildings(cursor)
	queries = []
	
	query = "SELECT city, building, completion FROM city_buildings"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['completion'] >= building_dict[row['building']].build_time:
			queries.append("UPDATE city_buildings SET amount = amount+1, completion = 0 WHERE city = %d AND building = %d" % (row['city'], row['building']))
	
	if verbose:
		if len(queries) > 1:
			print("cities_check.check_for_amount() found %d buildings to complete" % len(queries))
		elif len(queries) == 1:
			print("cities_check.check_for_amount() found 1 building to complete")
		else:
			print("cities_check.check_for_amount() found 0 buildings to complete")
	
	for q in queries:
		try:
			cursor.execute(q)
		except Exception as e:
			print("Query: %s\n" % query)
			raise e


def check_wonder_completion(cursor, verbose):
	completed, incomplete = [], []
	query = """SELECT id, point_cost, completion FROM wonders"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['point_cost'] <= row['completion']: completed.append(str(row['id']))
		else: incomplete.append(str(row['id']))
	
	# Complete them
	if completed != []:
		query = """UPDATE wonders SET completed = True WHERE id in (%s);""" % ",".join(completed)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Incomplete them
	if incomplete != []:
		query = """UPDATE wonders SET completed = False WHERE id in (%s);""" % ",".join(incomplete)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if verbose:
		print("cities_check.check_wonder_completion() checked the completion of all %d wonders" % (len(completed) + len(incomplete)))


def build_supplies(cursor, verbose):
	city_dict = city_q.get_live_cities(cursor)
	city_supply_dict = {}
	
	for k, v in city_dict.items():
		v.icon_size = map_data.map_image_size(v.population+v.slaves)/4
	
	if verbose:
		it = cli_f.progressbar(map_resources.data_list, "cities_check.build_supplies: ", 40, with_eta = True)
	else:
		it = map_resources.data_list
	
	for r, x, y in it:
		this_city = (-1, 9999)
		
		for k, v in city_dict.items():
			dist = path_f.pythagoras((v.x, v.y), (x, y))
			if dist < v.icon_size:
				if this_city[1] > v.founded:
					this_city = (k, v.founded)
		
		if this_city[0] > 0:
			if this_city[0] not in city_supply_dict:
				city_supply_dict[this_city[0]] = []
			city_supply_dict[this_city[0]].append(r)
	
	query = "UPDATE cities SET str_supplies = '';"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for k, v in city_supply_dict.items():
		vset = [str(r) for r in set(v)]
		
		query = "UPDATE cities SET str_supplies = '{0}' WHERE id = {1:d};".format(
			",".join(vset), k,
		)
		
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))


def overlapping_cities(cursor, verbose):
	city_dict = city_q.get_live_cities(cursor)
	
	checked = []
	overlap_dict = {}
	
	for id1, c1 in city_dict.items():
		c1.overlap = 0
	
	# Cache some stuff
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "cities_check.overlapping_cities: ", 40, with_eta = True)
	else:
		it = city_dict.items()
	
	for id1, c1 in it:
		checked.append(id1)
		
		for id2, c2 in city_dict.items():
			if id2 in checked: continue
			
			amount = city_f.overlap(c1, c2)
			
			c1.overlap += city_f.overlap_percentage(c1, amount)
			c2.overlap += city_f.overlap_percentage(c2, amount)
	
	# Reset all cities
	query = """UPDATE cities SET overlap = 0"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	updates = 0
	for id1, c1 in city_dict.items():
		if c1.overlap >= 1:
			updates += 1
			
			query = "UPDATE cities SET overlap = %d WHERE id = %d;" % (c1.overlap, id1)
			# print("%s - %s" % (query, c1.name))
			# continue
			
			try: cursor.execute(query)
			except Exception as e:
				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	


def city_terrain(cursor, verbose):
	queries = []
	city_dict = city_q.get_live_cities(cursor)
	
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "cities_check.city_terrain: ", 40, with_eta = True)
	else:
		it = city_dict.items()
	
	for k, c in it:
		t = mapper_q.get_terrain(cursor, c.x, c.y)
		
		if t != c.terrain:
			queries.append("UPDATE cities SET terrain = %d WHERE id = %d;" % (t, k))
	
	database.query(cursor, *queries)

def city_wealth(cursor, verbose):
	queries = []
	
	w = world.World(database.get_cursor())
	city_f.apply_city_matrix(w, compress=False)
	
	if verbose:
		it = cli_f.progressbar(w.live_cities().items(), "cities_check.city_wealth: ", 40, with_eta = True)
	else:
		it = w.live_cities().items()
	
	for k, c in it:
		c.wealth = city_rules.wealth_rate(w, c)
		queries.append("UPDATE cities SET wealth = %d WHERE id = %d;" % (c.wealth, k))
	
	database.query(cursor, *queries)

def trade_build(cursor, verbose):
	w = world.World(cursor)
	trade_f.build_distance_matrix(w, verbose)

def get_happiness(cursor, verbose):
	w = world.World(cursor)
	
	if verbose:
		it = cli_f.progressbar(w.live_cities().items(), "cities_check.get_happiness: ", 40, with_eta = True)
	else:
		it = w.live_cities().items()
	
	queries = []
	for city_id, the_city in it:
		queries.append("UPDATE cities SET happiness = %d WHERE id = %d;" % (city_rules.get_happiness(w, the_city), city_id))
	
	database.query(cursor, *queries)
	

def run(cursor, check_all, verbose):
	city_terrain(cursor, verbose)
	check_for_dead_cities(cursor, verbose)
	check_for_amount(cursor, verbose)
	check_wonder_completion(cursor, verbose)
	build_supplies(cursor, verbose)
	overlapping_cities(cursor, verbose)
	
	if check_all:
		trade_build(cursor, verbose)
	
	city_wealth(cursor, verbose)
	get_happiness(cursor, verbose)
	
	if verbose:
		print(database.shell_text("[g]City checks complete[/g]"))