import database
import collections
from classes import team
from classes import unit
from classes import res_dict
from classes import stat

def _team_query(cursor,
				where = '',
				orderby = 'active DESC, ir ASC, name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM teams"
	
	# Where
	if where != '': query += " WHERE %s" % where
	
	# Order by
	if orderby != '': query += " ORDER BY %s" % orderby
	
	# Limit stuff
	if start > 0 and limit > 0: query += " LIMIT %s, %s" % (start, limit)
	if start > 0 and limit < 1: query += " LIMIT 0, %s" % (limit)
	if start < 1 and limit > 0: query += " LIMIT %s" % (limit)
	
	results = collections.OrderedDict()
	try:
		cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['id']] = team.Team(row)
	
	return results

def get_all_teams(cursor):
	return _team_query(cursor=cursor)
	
def get_real_teams(cursor):
	return _team_query(where="not_a_team = False AND not_in_queue = False AND dead = False", cursor=cursor)

def get_real_active_teams(cursor, skip_irs=True):
	if skip_irs:
		return _team_query(where="not_a_team = False AND not_in_queue = False AND dead = False AND active = True AND ir = False", cursor=cursor)
	else:
		return _team_query(where="not_a_team = False AND not_in_queue = False AND dead = False AND active = True", cursor=cursor)

def get_one_team(cursor, the_team):
	if int(the_team) > 0:
		query = "SELECT * FROM teams WHERE id = {0:d} LIMIT 1;".format(int(the_team))
	else:
		query = "SELECT * FROM teams WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_team))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return team.Team(row)


def get_latest_active_team_id(cursor, skip_irs = True):
	if skip_irs:
		query = "SELECT id FROM teams WHERE active = True AND ir = False ORDER BY id LIMIT 1;"
	else:
		query = "SELECT id FROM teams WHERE active = True ORDER BY id LIMIT 1;"
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['id']

def get_next_active_team_id(cursor, current_id = -1, skip_irs = True):
	if current_id < 1:
		current_id = get_latest_active_team_id(cursor) - 1
	
	if skip_irs:
		query = "SELECT id FROM teams WHERE active = True AND id > %s AND ir = False ORDER BY id LIMIT 1;" % (current_id)
	else:
		query = "SELECT id FROM teams WHERE active = True AND id > %s ORDER BY id LIMIT 1;" % (current_id)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['id']
	
	return 0

def active_team_count(cursor, skip_irs = True):
	if skip_irs:
		query = "SELECT COUNT(*) FROM teams WHERE active = True AND ir = False;"
	else:
		query = "SELECT COUNT(*) FROM teams WHERE active = True;"
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['count']
	
	return 0

def get_borders(cursor):
	raise Exception("No longer living function")

def get_relations(cursor):
	# def constant_factory(value):
	# 	return lambda: value
	
	defaults = {}
	relations = {}
	query = """SELECT id, default_borders, default_taxes FROM teams"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		# defaults[row['id']] = row
		relations[row['id']] = {}
	
	# [Host][Visitor]
	query = """SELECT * FROM team_relations"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['border'] < 0:	del(row['border'])
		if row['taxes'] < 0:	del(row['taxes'])
		
		relations[row['host']][row['visitor']] = row
	
	return relations

def get_border_history(cursor):
	# [Host][Visitor]
	border_history = {}
	query = """SELECT host, visitor, state FROM border_history"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['host'] not in border_history:
			border_history[row['host']] = {}
		
		border_history[row['host']][row['visitor']] = row['state']
	
	return border_history

def get_army_size(cursor, team_id):
	return get_unit_category_size(cursor, team_id, 0, 6)

def get_navy_size(cursor, team_id):
	return get_unit_category_size(cursor, team_id, 7)

def get_airforce_size(cursor, team_id):
	return get_unit_category_size(cursor, team_id, 8)

def get_unit_category_size(cursor, team_id, cat_min, cat_max=None):
	amount = 0
	
	if cat_max == None:
		cat_max = cat_min
	
	# unit.categories[6] is the last land unit category
	query = """SELECT s.amount
		FROM units u, squads s
		WHERE s.team = {team_id}
			AND s.unit = u.id
			AND u.type_cat >= {cat_min} AND u.type_cat <= {cat_max}""".format(
			team_id=team_id,
			cat_min=cat_min,
			cat_max=cat_max,
		)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		amount += row['amount']
	
	return amount

def get_mage_count(cursor, team_id):
	amount = 0
	
	# unit.categories[6] is the last land unit category
	query = """SELECT amount
		FROM squads
		WHERE team = {team_id}
			AND unit <= 20""".format(
			team_id=team_id,
		)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		amount += row['amount']
	
	return amount

def mass_get_team_spells(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.spell_levels	= {}
		the_team.spell_points	= {}
	
	query = "SELECT spell, points, level, team FROM team_spells"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].spell_levels[row['spell']] = row['level']
		team_dict[row['team']].spell_points[row['spell']] = row['points']
	
	return team_dict

def mass_get_team_techs(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.tech_levels	= {}
		the_team.tech_points	= {}
	
	query = "SELECT tech, points, level, team FROM team_techs"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].tech_levels[row['tech']] = row['level']
		team_dict[row['team']].tech_points[row['tech']] = row['points']
	
	return team_dict


def mass_get_team_deities(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.deities	= {}
	
	query = "SELECT deity, favour, team FROM team_deities"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].deities[row['deity']] = row['favour']
	
	return team_dict

def mass_get_team_resources(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.resources = res_dict.Res_dict()
	
	query = "SELECT team, resource, amount FROM team_resources"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].resources.value[row['resource']] = row['amount']
	
	return team_dict

def mass_get_team_evolutions(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.evolutions = {}
	
	query = "SELECT team, evolution, level FROM team_evolutions"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].evolutions[row['evolution']] = row['level']
	
	return team_dict

def mass_get_artefacts(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.artefacts = []
	
	query = "SELECT team, id FROM artefacts"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].artefacts.append(row['id'])
	
	return team_dict

def mass_get_team_traits(cursor, team_dict):
	for k, the_team in team_dict.items():
		the_team.traits = []
	
	query = "SELECT team, trait FROM team_traits"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].traits.append(row['trait'])
	
	return team_dict

def mass_get_team_stats(cursor, team_dict, turn):
	for k, the_team in team_dict.items():
		# First we need to wipe the placeholder, otherwise we're good to go
		if the_team.stats == {"Checked":False}: the_team.stats = {}
	
	query = "SELECT * FROM team_stats WHERE turn = %d" % int(turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['team'] not in team_dict: continue
		team_dict[row['team']].stats[turn] = stat.Stat(row)
	
	return team_dict
