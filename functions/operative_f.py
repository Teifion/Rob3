import math
import database
from random import randint
from pages import common
from classes import spy_report
from functions import spy_report_f

chars = [str(c) for c in range(0,10)]

def new_operative(city, team, arrival, size, stealth, observation, integration, sedition, sabotage, assassination, name=""):
	if name == "":
		name = "".join([chars[randint(0,9)] for c in range(0, 6)])
		
		if team < 100:
			name = "00%s%s" % (str(team)[0:2], name)
		elif team < 1000:
			name = "0%s%s" % (str(team)[0:3], name)
		else:
			name = "%s%s" % (str(team)[0:4], name)
	
	return """INSERT INTO operatives (name, city, team, arrival, size, stealth, observation, integration, sedition, sabotage, assassination)
		values
		('%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d);""" % (database.escape(name), city, team, arrival, size, stealth, observation, integration, sedition, sabotage, assassination)

def move_operative_query(op_id, city_id):
	return ["""UPDATE operatives SET city = %d, arrival = %d WHERE id = %d;""" % (city_id, common.current_turn(), op_id)]

def kill_operative(operative_id):
	return "UPDATE operatives SET died = %d WHERE id = %d;" % (common.current_turn(), operative_id)

def revive_operative(operative_id):
	return "UPDATE operatives SET died = 0 WHERE id = %d;" % (operative_id)
	
def delete_operative(operative_id):
	return """DELETE FROM operatives WHERE id = %s;""" % (operative_id)

def recruitment_query(name, city, team, stats):
	return [new_operative(city, team, common.current_turn(),
		stats['Size'], stats['Stealth'], stats['Observation'], stats['Integration'],
		stats['Sedition'], stats['Sabotage'], stats['Assassination'], name)]

def reinforce_query(op_id, amount):
	return ["UPDATE operatives SET size = size + %d, arrival = %d WHERE id = %d;" % (amount, op_id, common.current_turn())]

def catch_operatives(the_world, verbose=False):
	relations	= the_world.relations()# [Host][Visitor]
	operative_dict = the_world.operatives()
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	
	# Get list of all operatives in cities where they're in cities they are not meant to be
	hostile_ops = []
	for op_id, the_op in operative_dict.items():
		if the_op.died > 0: continue
		
		if city_dict[the_op.city].team != the_op.team:
			try:
				host_team = team_dict[city_dict[the_op.city].team]
				if relations.get(host_team.id, {}).get(the_op.team, {}).get('borders', host_team.default_borders) < spy_report.friendly_border:
					# Ensure that they are at least seggregated (and thus want to catch you)
					hostile_ops.append(op_id)
			except Exception as e:
				print(the_op.city)
				print(city_dict[the_op.city].team)
				print(the_op.team)
				print(borders)
				raise

	
	capture_list = []
	for o in hostile_ops:
		c = capture_chance(the_world, o)
		caught = spy_report_f._success(c)
		
		if verbose:
			if caught:
				caught_str = database.shell_text(" - [r]Caught[/r]")
			else:
				caught_str = ""
			
			print("Id: {id}, Chance: {c}%, City: {city}{caught_str}".format(
				id=o,
				c=round(c*100,3),
				city=city_dict[operative_dict[o].city].name,
				caught_str=caught_str,
			))
		
		if caught:
			capture_list.append(str(o))
	
	if verbose:
		print("Caught %d out of %d ops" % (len(capture_list), len(hostile_ops)))
	
	if len(capture_list) > 0:
		# Update capture status
		query = """UPDATE operatives SET died = %d WHERE id in (%s);""" % (common.current_turn(), ",".join(capture_list))
		try: the_world.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				
	
min_catch_chance = 0.0001
def capture_chance(the_world, op_id):
	# relations	= the_world.relations()# [Host][Visitor]
	the_op = the_world.operatives()[op_id]
	op_dict = the_world.operatives()
	the_city = the_world.cities()[the_op.city]
	team_dict = the_world.teams()
	
	# Aliases
	covert_centre = the_world.buildings_lookup()['Covert centre']
	covert_tech = the_world.techs_lookup()['Covert training']
	
	operatives_in_city = the_world.operatives_in_city(the_city.id)
	
	allied_ops, hostile_ops = spy_report._op_lists_city(the_world, the_op.team, the_city.id)
	
	# Allied aid is the sum of their observation
	allied_score = 0
	for o in allied_ops:
		age = 1 + math.sqrt(common.current_turn() - o.arrival) * 0.1
		allied_score += o.observation * o.size * age
	
	# Hostile score is the sum of the squares of observation
	hostile_score = 0
	for o in hostile_ops:
		age = 1 + math.sqrt(common.current_turn() - o.arrival) * 0.1
		hostile_score += o.observation * o.size * age
	
	# Now we bring into account the operative in question
	diff = the_world.race_difference(the_op.team, the_city.team)
	diff = ((diff/10) - the_op.integration)/10# Can range from 1 to -0.5
	diff = max(diff, -0.5)
	diff += 1# Now ranges from 2 to 0.5
	
	hostile_score *= diff# Poor integration and a high physical difference means massive boost to hostile score
	
	# Covert centre?
	if covert_centre in the_city.buildings_amount and the_city.buildings_amount[covert_centre] > 0:
		hostile_score *= 1.3
	
	age = 1 + math.sqrt(common.current_turn() - o.arrival) * 0.1
	allied_score *= (the_op.stealth * age)
	allied_score *= ((team_dict[the_op.team].tech_levels.get(covert_tech, 0) * 0.03)+1)
	
	if allied_score > hostile_score:
		res = min_catch_chance
	else:
		if allied_score == 0:
			res = 1
		else:
			res = (hostile_score/allied_score)
			# res *= (hostile_score-allied_score)
			res /= 100
			res += min_catch_chance
	
	return res

