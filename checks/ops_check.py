import database
from queries import team_q, operative_q, city_q
from functions import cli_f
from pages import common

def check_operative_locations(cursor, verbose):
	"""Finds operatives in dead cities and relocates them"""
	teams_dict			= team_q.get_all_teams(cursor)
	operatives_dict		= operative_q.get_all_operatives(cursor)
	city_dict			= city_q.get_all_cities(cursor)
	
	# Get a list of the dead cities
	dead_city_list = []
	for c_id, the_city in city_dict.items():
		if the_city.dead > 0 or not teams_dict[the_city.team].active:
			dead_city_list.append(str(c_id))
	
	# Find operatives in those cities
	query = """SELECT id FROM operatives WHERE city in (%s) and died < 1""" % ",".join(dead_city_list)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	move_op_list = {}
	for row in cursor:
		o = row['id']
		t = operatives_dict[o].team
		
		if not teams_dict[t].active: continue
		
		if t not in move_op_list:
			move_op_list[t] = []
		
		move_op_list[t].append(str(o))
	
	# Find out which teams we need to get a city for
	teams_cities = {}
	for t in move_op_list.keys():
		teams_cities[t] = -1
	
	# Find cities for those teams
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "ops_check.check_operative_locations: ", 40, with_eta = True)
	else:
		it = city_dict.items()
	
	for c_id, the_city in it:
		if the_city.team in teams_cities and not teams_dict[the_city.team].dead:
			teams_cities[the_city.team] = c_id
	
	# Now run the queries
	queries = []
	for t, c in teams_cities.items():
		query = "UPDATE operatives SET city = %d, arrival = %d WHERE id in (%s)" % (
			c,
			common.current_turn(),
			",".join(move_op_list[t]),
		)
	
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

	

def run(cursor, check_all, verbose):
	check_operative_locations(cursor, verbose)
	
	if check_all:
		pass
	
	if verbose:
		print(database.shell_text("[g]Operative checks complete[/g]"))