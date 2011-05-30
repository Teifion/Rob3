from hashlib import md5
import database
from queries import unit_q, team_q
from rules import unit_rules, team_rules, military_rules
import rules
import pages
from lists import resource_list
from classes import unit, res_dict
from functions import log_f
import os
import time

def structured_list(cursor, include_irs = True, active_only = True, default=-1, field_name="team", field_id="", skip=[]):
	if include_irs:
		ir_query = ""
	else:
		ir_query = "AND ir = False"
	
	if active_only:
		active_query = "AND active = True"
	else:
		active_query = ""
	
	results = []
	
	last_team_was_active = True
	
	query = """SELECT id, name, active
		FROM teams
			WHERE not_a_team = False %s %s
				AND not_in_queue = False
				ORDER BY active DESC, name ASC""" % (ir_query, active_query)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['id'] in skip: continue
		if last_team_was_active == True and row['active'] == False:
			results.append('<option disabled="disabled" value="-1">&nbsp;</option>')
			last_team_was_active = False
		
		selected = ""
		if row['id'] == default:
			selected = 'selected="selected"'
		
		results.append('<option value="%d"%s>%s</option>' % (row['id'], selected, row['name']))
	
	id_string = ""
	if field_id != "":
		id_string = 'id="%s"' % field_id
	
	return """<select name="%s" %s>
	%s
	</select>""" % (field_name, id_string, "".join(results))

def add_deity(team, deity):
	team = int(team)
	deity = int(deity)
	
	return "INSERT INTO team_deities (team, deity) values ({0:d}, {1:d});".format(team, deity)

def remove_deity(team, deity):
	team = int(team)
	deity = int(deity)
	
	return "DELETE FROM team_deities WHERE team = {0:d} AND deity = {1:d};".format(team, deity)

def add_trait(team, trait):
	team = int(team)
	trait = int(trait)
	
	return "INSERT INTO team_traits (team, trait) values ({0:d}, {1:d});".format(team, trait)

def remove_trait(team, trait):
	team = int(team)
	trait = int(trait)
	
	return "DELETE FROM team_traits WHERE team = {0:d} AND trait = {1:d};".format(team, trait)

def set_evolution(team, evolution, level=0, evo_cost=0):
	"""Adds an evolution to a team"""
	if team < 0 or evolution < 0: return
	
	queries = []
	
	if level == 0:
		queries.append("DELETE FROM team_evolutions WHERE team = %d AND evolution = %d" % (team, evolution))
	else:
		queries.append("DELETE FROM team_evolutions WHERE team = %d AND evolution = %d" % (team, evolution))
		queries.append("""INSERT INTO team_evolutions (team, evolution, level)
			values (%d, %d, %d)""" % (team, evolution, level))
	
	if evo_cost != 0:
		queries.append("UPDATE teams SET evo_points = evo_points - %d WHERE id = %d;" % (evo_cost, team))
	
	return queries

def set_resources(cursor, team_id, resource_dict):
	team_id = int(team_id)
	
	# Delete the resources first
	query = "DELETE FROM team_resources WHERE team = %d" % (team_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	res_updates = []
	for k, v in resource_dict.items():
		res_updates.append("(%s, %s, %s)" % (k, v, team_id))
	
	# Now to update it
	return "INSERT INTO team_resources (resource, amount, team) values %s;" % ",".join(res_updates)

def team_hash(name, turn=-1, passcode="my_passcode"):
	from pages import common
	
	if turn == -1:
		turn = common.current_turn()
	
	m = md5()
	m.update(passcode.encode("utf-8"))
	m.update(name.encode("utf-8"))
	m.update(str(turn).encode("utf-8"))
	return m.hexdigest()

	
def grow_cities(the_world, the_team):
	# return grow_cities_old(the_world, the_team)
	from pages import common
	from functions import path_f
	from functions import queries_f
	queries = []
	
	"""Grows all the cities for the team"""
	city_dict = the_world.cities_from_team(the_team.id)
	
	team_rules.Food(the_world.cursor, the_team, the_world=the_world)
	modifier = team_rules._food_needed_modifier(the_world, the_team)
	
	# First work out how much food they have
	for city_id, the_city in city_dict.items():
		if the_city.dead > 0: continue
		the_city.surplus_food = ((the_city.surplus_food/1000) - (the_city.size * modifier))*1000
	
	# Now we go and try to redistribute the food a bit
	logs = []
	for city_id, the_city in city_dict.items():
		if the_city.dead > 0: continue
		
		if the_city.surplus_food < 0:
			for city_id2, city2 in city_dict.items():
				if the_city.surplus_food >= 0: continue
				if city2.surplus_food <= 0: continue
				# if path_f.pythagoras(the_city, city2) > 1000: continue# More than 1k map units
				
				if city2.surplus_food > abs(the_city.surplus_food):
					# 2nd city has more than enough food
					city2.surplus_food += the_city.surplus_food
					the_city.surplus_food = 0
				else:
					# 2nd city can get us some of the way
					the_city.surplus_food += city2.surplus_food
					city2.surplus_food = 0
		
		growth_rate, growth_constant = rules.city_rules.city_growth_rate(the_world.cursor, the_team, the_city, the_world)
		new_population = int((the_city.population * growth_rate) + growth_constant)
		
		if new_population < 1:
			logs.append("Kill %s (id: %d) as pop = %d" % (the_city.name, city_id, new_population))
			queries.append("""UPDATE cities SET dead = %d WHERE id = %d;""" % (common.current_turn(), city_id))
		else:
			logs.append("Grow %s (id: %d) to %s, old pop: %d, old slave: %d, rate: %d, constant: %d" % (
				the_city.name, city_id, new_population, the_city.population, the_city.slaves, growth_rate, growth_constant)
			)
			queries.extend([
				"-- Growing city %d, old pop: %d, old slave: %d, new pop, %d, rate: %d, constant: %d" % (
					city_id, the_city.population, the_city.slaves, new_population, growth_rate, growth_constant,
				),
				"""UPDATE cities SET population = %d WHERE id = %d;""" % (new_population, city_id),
			])
	
	
	database.query(the_world.cursor, 
		log_f.new_log("team_f.grow_cities", "\n".join(logs), "", team = the_team.id)
	)
	
	# for q in queries:
	# 	try:
	# 		queries_f.log_query(the_world.cursor, q, subject="Growing cities")
	# 		the_world.cursor.execute(q)
	# 	except Exception as e:
	# 		print("Query: %s\n" % q)
	# 		raise e
	try:
		database.query(
			the_world.cursor, queries
		)
	except Exception as e:
		print("Queries: %s\n" % "\n".join(queries))
		raise e
	
	return queries

def grow_cities_old(the_world, the_team):
	from rules import city_rules
	
	"""Grows all the cities for the team"""
	city_dict = the_world.cities_from_team(the_team.id)
	
	for city_id, the_city in city_dict.items():
		if the_city.dead > 0: continue
		
		growth_rate, growth_constant = rules.city_rules.city_growth_rate(the_world.cursor, the_team, the_city, the_world)
		
		new_population = int((the_city.population * growth_rate) + growth_constant)
		
		# if new_population < 1:
		# 	query = """UPDATE cities SET dead = True WHERE id = %d;""" % (city_id)
		# else:
		# 	query = """UPDATE cities SET population = %d WHERE id = %d;""" % (new_population, city_id)
		# 
		# try: the_world.cursor.execute(query)
		# except Exception as e:
		# 	raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		print(growth_rate)


def record_favour(the_world, the_team):
	from rules import deity_rules
	
	deity_dict = the_world.deities()
	the_team.get_deities(the_world.cursor)
	
	for d in the_team.deities.keys():
		new_favour, favour_desc = deity_rules.calculate_favour(the_world, the_team, d)
		
		query = """UPDATE team_deities SET favour = %d
			WHERE team = %d AND deity = %d;""" % (int(new_favour), int(the_team.id), int(d))
		try: the_world.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		# Log favour
		database.query(the_world.cursor, 
			log_f.new_log("team_f.record_favour", "Deity: %d, Favour: %d, Desc: %s" % (int(d), int(new_favour), favour_desc), "", team = the_team.id)
		)
		
		# Update team item too
		the_team.deities[d] = new_favour


def produce_resources(the_world, the_team):
	"""Produces resources for the coming turn"""
	# Get production
	upkeep_cost = get_upkeep(the_team, the_world)
	database.query(the_world.cursor, 
		log_f.new_log("team_f.get_upkeep", "Upkeep: %s" % upkeep_cost, "", team = the_team.id)
	)
	
	produced_resources, new_resources = rules.team_rules.produce_resources(
		the_world.cursor, the_team, the_world=the_world
	)
	
	# Log production
	database.query(the_world.cursor, 
		log_f.new_log("team_f.produce_resources", "Produced: %s\nNew: %s" % (str(produced_resources), str(new_resources)), "", team = the_team.id)
	)
	
	# Apply upkeep
	new_resources -= "Materials:%s" % upkeep_cost
	
	queries = new_resources.make_set_queries(the_team.id)
	
	from functions import queries_f
	
	for q in queries:
		try:
			queries_f.log_query(the_world.cursor, q, subject="Pre orders resources")
			the_world.cursor.execute(q)
		except Exception as e:
			print("Query: %s\n" % q)
			raise e
	
	return queries


def get_upkeep(the_team, the_world):
	"""Returns the upkeep cost of the nation's army"""
	# We need to do this on a per-army basis now
	unit_dict = the_world.units()
	army_dict = the_world.armies()
	squad_dict = the_world.squads_from_team(the_team.id)
	city_dict = the_world.cities_from_team(the_team.id)
	
	the_world.mass_get_city_buildings()
	
	# Cache iron, makes it faster
	the_team.get_resources(the_world.cursor)#force_requery=True)
	if the_team.resources.get("Iron") > 0:
		has_iron = True
	else:
		has_iron = False
	
	military_upkeep = 0
	for squad_id, the_squad in squad_dict.items():
		if the_squad.amount < 1: continue
		
		the_unit = unit_dict[the_squad.unit]
		the_army = army_dict[the_squad.army]
		
		# Don't wanna pay upkeep for units that are not ours!
		if the_unit.team != 0 and the_unit.team != the_team.id:
			continue
		
		# Get Iron/Material cost
		if has_iron:
			unit_cost = the_unit.get_cost(cursor=the_world.cursor, the_world=the_world)['material_upkeep'].get("Materials", 0)
		else:
			unit_cost = the_unit.get_cost(cursor=the_world.cursor, the_world=the_world)['iron_upkeep'].get("Materials", 0)
		
		# Upkeep override for things like magical affinity
		unit_cost = unit_rules.unit_upkeep_override(the_world, the_unit, unit_cost, the_team)
		
		# If it's a ship or airship we don't divide by the divisor
		if the_unit.type_cat == unit.categories.index("Ship") or \
			the_unit.type_cat == unit.categories.index("Airship"):
			temp_cost = (unit_cost * the_squad.amount)
		else:
			temp_cost = (unit_cost * the_squad.amount/military_rules.amount_divisor)
		
		# Now we take into account the army type
		if the_army.garrison > 0:
			temp_cost *= military_rules.garrison_upkeep
		else:
			temp_cost *= military_rules.army_upkeep
		
		# Used for debugging
		if temp_cost > 0:
			pass
			# print "%s: %s * %s = %s<br />" % (unit_dict_c[unit_id].name, unit_cost, unit_count, temp_cost)
		
		# if the_army.name == "Kan Putri garrison":
		# 	print(the_squad.name, str(temp_cost), "<br />")
		
		military_upkeep += temp_cost
	
	# exit()
	
	# Now for buildings
	building_upkeep = 0
	# building_upkeep_dict = {}
	# for k, b in the_world.buildings().items():
	# 	building_upkeep_dict[k] = res_dict.Res_dict(b.upkeep)['Materials']
	# 
	# for city_id, the_city in city_dict.items():
	# 	for building_id, amount in the_city.buildings_amount.items():
	# 		building_upkeep += amount * building_upkeep_dict[building_id]
	
	# print str(the_team.resources), " - ", total_cost, "<br />"
	military_upkeep = team_rules.alter_upkeep(the_world.cursor, the_team, military_upkeep, the_world)
	return military_upkeep + building_upkeep


def record_resources(the_world, the_team):
	"""Records the end of turn resources for the team"""
	the_team.get_resources(the_world.cursor, force_requery=True)
	
	strings = []
	
	for res_id, r in enumerate(resource_list.data_list):
		if res_id not in the_team.resources.value: continue
		if the_team.resources.value[res_id] == 0: continue
		if r.reset: continue
		
		res_value = the_team.resources.value[res_id]
		
		# Typecast if we can
		if res_value == int(res_value):
			res_value = int(res_value)
		
		strings.append("%s:%s" % (r.name, res_value))
	
	# Log previous resources
	database.query(the_world.cursor, 
		log_f.new_log("team_f.record_resources", ",".join(strings), "", team = the_team.id)
	)
	
	query = """UPDATE teams SET previous_resources = '%s' WHERE id = %d;""" % (database.escape(",".join(strings)), the_team.id)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

def get_battle_losses(the_world, the_team, turn=0):
	from queries import battle_q
	
	if turn < 1:
		turn = pages.common.current_turn()
	
	output = ["[o]Losses[/o]\n"]
	
	# team_units		= the_team.get_units()
	squad_dict		= the_world.squads()
	team_dict		= the_world.teams()
	unit_dict		= the_world.units()
	
	# Get a list of all the campaigns this team was part of this turn
	campaign_list = []
	query = """SELECT c.id
		FROM campaign_teams ct, campaigns c
			WHERE ct.team = %d
			AND ct.campaign = c.id
			AND c.turn = %d""" % (the_team.id, turn)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in the_world.cursor:
		campaign_list.append(str(row['id']))
	
	# No campaigns, no losses
	if campaign_list == []:
		return ""
	
	# Now we need a list of all the battles in this campain
	battle_list = []
	battle_dict = {}
	query = "SELECT id, name FROM battles WHERE campaign in (%s)" % ",".join(campaign_list)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in the_world.cursor:
		battle_dict[row['id']] = row['name']
		battle_list.append(str(row['id']))
	
	# No battles, no section of results here!
	if battle_list == []:
		return ""
	
	# Now for a list of all squad losses, sort by battle
	query = """SELECT squad, battle, losses
		FROM squad_battle_history
			WHERE battle IN (%s)
				ORDER BY battle""" % ",".join(battle_list)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	losses = {"Total":{}}
	for row in the_world.cursor:
		if row['losses'] == 0: continue
		
		if row['battle'] not in losses:
			losses[row['battle']] = {}
		
		the_squad = squad_dict[row['squad']]
		
		if the_squad.team != the_team.id: continue
		if the_squad.unit not in losses[row['battle']]:
			losses[row['battle']][the_squad.unit] = 0
		
		if the_squad.unit not in losses["Total"]:
			losses["Total"][the_squad.unit] = 0
		
		losses[row['battle']][the_squad.unit] += row['losses']
		losses["Total"][the_squad.unit] += row['losses']
	
	for b, battle_name in battle_dict.items():
		if b == "Total" or b not in losses: continue
		output.append("[b]%s[/b]\n" % battle_name)
		for u, a in losses[b].items():
			output.append("%s: %s\n" % (unit_dict[u].name, a))
		
		output.append("")
	
	if len(battle_dict) > 1:
		output.append("[b]Total losses[/b]\n")
		for u, a in losses["Total"].items():
			output.append("%s: %s\n" % (unit_dict[u].name, a))
		
	return "".join(output)

def create_results_tail(the_world, the_team):
	results = []
	
	#	LOSSES
	#------------------------
	results.append(get_battle_losses(the_world, the_team))
	
	'''
	#	RESOURCES
	#------------------------
	produced_resources, new_resources = rules.team_rules.produce_resources(the_world.cursor, the_team, the_world)
	the_team.get_resources(the_world.cursor, force_requery=True)
	
	the_team.previous_dict = res_dict.Res_dict(the_team.previous_resources)
	'''
	
	return "\n".join(results)

def pre_orders(the_world, the_team):
	from functions import stat_f
	
	# Team stats
	# stat_f.build_team_stats(the_world.cursor, the_team, the_world)
	
	# Record current favour
	record_favour(the_world, the_team)
	
	# Recored current resources
	record_resources(the_world, the_team)
	
	# Produce resources
	if not the_team.ir:
		produce_resources(the_world, the_team)
	
	# Grow cities
	if not the_team.ir:
		grow_cities(the_world, the_team)


def border_history(the_world):
	team_dict = the_world.teams()
	borders = {}
	
	# [Host][Visitor]
	for team_id, the_team in team_dict.items():
		borders[team_id] = {-1:the_team.default_borders}
	
	query = """SELECT host, visitor, border FROM team_relations"""
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in the_world.cursor:
		borders[row['host']][row['visitor']] = row['border']
	
	# Delete old history
	query = """DELETE FROM border_history"""
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Insert new
	inserts = []
	for host, states in borders.items():
		for visitor, state in states.items():
			inserts.append("(%s, %s, %s)" % (host, visitor, state))
	
	query = """INSERT INTO border_history (host, visitor, state)
		values
		%s;""" % ",".join(inserts)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# print(query)

def open_int_orders(cursor):
	from pages import common
	team_dict = team_q.get_real_active_teams(cursor)
	
	for team_id, the_team in team_dict.items():
		# time.sleep(0.25)
		
		if the_team.intorders_topic > 0:
			cmd = "open http://localhost/rob3/web.py?mode=view_intorders\\&turn={turn}\\&team={team}\\&topic_id={topic}".format(
				turn = common.current_turn(),
				team = team_id,
				topic = the_team.intorders_topic,
			)
			os.system(cmd)
			# print(cmd)

def open_results(cursor):
	from pages import common
	team_dict = team_q.get_real_active_teams(cursor)

	for team_id, the_team in team_dict.items():
		if the_team.results_topic > 0:
			cmd = "open http://woarl.com/board/viewtopic.php?t={topic}".format(
				topic = the_team.results_topic,
			)
			os.system(cmd)
			# print(cmd)

def make_team_relation(host, visitor):
	return ["INSERT INTO team_relations (host, visitor) values (%d, %d)" % (host, visitor)]

def make_default_borders(team_id, state):
	return ["UPDATE teams SET default_borders = %d WHERE id = %d;" % (state, team_id)]

def specific_borders_reset(host, visitor):
	return ["UPDATE team_relations SET border = -1 WHERE host = %d AND visitor = %d;" % (host, visitor)]

def make_specific_borders(host, visitor, state):
	return ["UPDATE team_relations SET border = %d WHERE host = %d AND visitor = %d;" % (state, host, visitor)]


def make_default_taxes(team_id, rate):
	return ["UPDATE teams SET default_taxes = %d WHERE id = %d;" % (rate, team_id)]

def specific_taxes_reset(host, visitor):
	return ["UPDATE team_relations SET taxes = -1 WHERE host = %d AND visitor = %d;" % (host, visitor)]

def make_specific_taxes(host, visitor, rate):
	return ["UPDATE team_relations SET taxes = %d WHERE host = %d AND visitor = %d;" % (rate, host, visitor)]



