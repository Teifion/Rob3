# import random
# import time
# import database
# from pages import common
# from data import unit, equipment, squad
# from data import city, city_q, building
# from data import mission, mission_q, spy_report_f
# from data import team, team_q
# from rules import team_rules

def count_mission_requests(cursor):
	query = "SELECT COUNT(*) FROM missions WHERE state = 0"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['count']
	
	return 0

# def new_mission(team, turn, the_type, state, target):
# 	# Now to insert
# 	query = """INSERT INTO missions (team, turn, type, state, target, time_posted, information)
# 		values
# 		(%(team)s, %(turn)s, %(type)s, %(state)s, %(target)s, %(time_posted)s, '');""" % {
# 			"team":			team,
# 			"turn":			turn,
# 			"type":			the_type,
# 			"state":		state,
# 			"target":		target,
# 			"time_posted":	int(time.time()),
# 		}
# 	try: database.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

# Tries to adda a new mission via orders
# def orders_add_mission(the_team, the_type, target):
# 	# First we look to see if this mission already exists
# 	query = """SELECT id
# 		FROM missions
# 			WHERE team = %d AND type = %d AND target = %d
# 				AND (turn = %d OR state = %d)""" % (the_team, the_type, target, common.current_turn(), mission.mission_states.index('Pending result'))
# 	try: database.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
# 	
# 	mission_id = -1
# 	for row in database.cursor:
# 		mission_id = row['id']
# 	
# 	if mission_id > 0:
# 		return
# 	
# 	# It's not there already, lets add it!
# 	new_mission(the_team, common.current_turn(), the_type, mission.mission_states.index('Pending result'), target)

# def handle_mission(mission_id, info, caught_list):
# 	"""Sets the mission to be handled, posts the spy report to each team and """
# 	the_mission = mission.Mission(mission_q.get_one_mission(mission_id))
# 	our_team = team_q.get_one_team(the_mission.team)
# 	
# 	if mission.mission_types[the_mission.type] in mission.city_targets:
# 		the_city = city_q.get_one_city(the_mission.target)
# 		target_team = team_q.get_one_team(the_city['team'])
# 		target_string = "%s [i](%s)[/i]" % (the_city['name'], target_team['name'])
# 		
# 	elif mission.mission_types[the_mission.type] in mission.team_targets:
# 		target_team = team_q.get_one_team(the_mission.target)
# 		target_string = target_team['name']
# 	
# 	# Set the mission to "complete"
# 	query = """UPDATE missions
# 		SET state = %d, time_closed = %d
# 			WHERE id = %d;""" % (mission.mission_states.index('Result given'), int(time.time()), mission_id)
# 	try: database.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
# 	
# 	# Post reports
# 	if caught_list != []:
# 		if len(caught_list) == 1:
# 			content = "%s\n\nLosses: 1 operative" % info
# 		else:
# 			content = "%s\n\nLosses: %d operatives" % (info, len(caught_list))
# 	else:
# 		content = info
# 	
# 	spy_report_f.new_report(mission_id, team=our_team['id'], enemy=target_team['id'], content=content)
# 	
# 	# If someone was caught then we inform the people that caught them
# 	if caught_list != []:
# 		if len(caught_list) == 1:
# 			content = "1 operative from %s was caught trying to spy on you" % (our_team['name'])
# 		else:
# 			content = "%d operatives from %s were caught trying to spy on you" % (len(caught_list), our_team['name'])
# 		spy_report_f.new_report(mission_id, team=target_team['id'], enemy=our_team['id'], content=content)
# 	
# 	
# 	# Now to make the spies dead
# 	if caught_list != []:
# 		query = """UPDATE operatives SET died = %d WHERE id in (%s);""" % (common.current_turn(), 
# 			",".join([str(o) for o in caught_list]))
# 		try: database.cursor.execute(query)
# 		except Exception as e:
# 			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

# def city_general(target, fudge=0):
# 	return "Currently this doesn't do anything"

# def city_armies(target, fudge=0):
# 	return "Currently this doesn't do anything"

# def city_buildings(target, fudge=0):
# 	"""docstring for city_buildings"""
# 	city_dict_c		= city.get_city_dict_c()
# 	building_dict	= building.get_building_dict()
# 	
# 	the_city = city_dict_c[target]
# 	the_city.get_buildings()
# 	
# 	output = ["City buildings:"]
# 	for b, a in the_city.buildings_amount.items():
# 		if a > 0:
# 			if random.uniform(0, 100) >= fudge:
# 				output.append("%d %s" % (a, building_dict[b]))
# 	
# 	if output == []:
# 		output = ["%s has no buildings" % the_city.name]
# 	else:
# 		output.insert(0, "[b]Completed buildings at %s[/b]" % the_city.name)
# 		
# 	return "\n".join(output)

# def nation_morale(target, fudge=0):
# 	target_team		= team.Team(team_q.get_one_team(target))
# 	actual_morale	= team_rules.nation_morale(target_team)
# 	
# 	multiplier_max = 1 + (fudge/5.0)
# 	multiplier_min = 1 + (fudge/100.0)
# 	
# 	return_morale = actual_morale * random.uniform(multiplier_min, multiplier_max)
# 	
# 	return "Nation morale: %s" % team_rules.define_nation_morale(return_morale)

# def nation_military(target, fudge=0):
# 	unit_dict_c		= unit.get_unit_dict_c()
# 	equipment_dict	= equipment.get_equipment_dict()
# 	
# 	target_team = team.Team(team_q.get_one_team(target))
# 	target_team.get_units()
# 	
# 	units = {}
# 	for unit_id, the_unit in unit_dict_c.items():
# 		if the_unit.team != target:			continue
# 		
# 		unit_count = min(target_team.units.get(unit_id,0), 1000)/1.000
# 		if random.uniform(0, 100) <= fudge: continue
# 		if unit_count == 0: continue
# 		
# 		items = []
# 		
# 		the_unit.get_equipment()
# 		
# 		for e in the_unit.equipment:
# 			if random.uniform(25, 100) >= fudge:
# 				items.append(equipment_dict[e])
# 		
# 		units[unit_id] = items
# 	
# 	output = ["Nation military:"]
# 	for u, equ_list in units.items():
# 		if len(equ_list) > 1:
# 			output.append("%s are equipped with: %s and %s" % (unit_dict_c[u].name, ", ".join(equ_list[0:-1]), equ_list[-1]))
# 		else:
# 			output.append("%s are equipped with: %s" % (unit_dict_c[u].name, ", ".join(equ_list)))
# 	return "\n".join(output)

# mission_functions = {
# 	'City general':			city_general,
# 	'City armies':			city_armies,
# 	'City buildings':		city_buildings,
# 	'Nation morale':		nation_morale,
# 	'Military equipment':	nation_military,
# }