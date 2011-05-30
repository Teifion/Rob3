import database
import collections
from classes import battle
from pages import common

def _battle_query(cursor,
				where = '',
				orderby = 'start, name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM battles"
	
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
		results[row['id']] = battle.Battle(row)
	
	return results

def get_all_battles(cursor):
	return _battle_query(cursor)

def get_battles_from_campaign(cursor, campaign_id):
	return _battle_query(cursor, where="campaign=%d" % campaign_id)

def get_battles_from_turn(cursor, turn):
	query = "SELECT b.* FROM battles b, campaigns c WHERE c.turn = %d AND b.campaign = c.id" % turn
	results = collections.OrderedDict()
	try:
		cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['id']] = battle.Battle(row)
	
	return results

def get_one_battle(cursor, the_battle):
	if type(the_battle) == str:
		query = "SELECT * FROM battles WHERE name = '{0:s}' ORDER BY id DESC LIMIT 1;".format(database.escape(the_battle))
	else:
		query = "SELECT * FROM battles WHERE id = {0:d} LIMIT 1;".format(int(the_battle))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return battle.Battle(row)

def get_last_battle_from_campaign(cursor, campaign_id):
	query = "SELECT * FROM battles WHERE campaign = '{0:d}' ORDER BY start DESC LIMIT 1;".format(campaign_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return battle.Battle(row)

def get_all_battle_losses_by_squad(cursor, battle_id):
	query = """SELECT squad, losses FROM squad_battle_history WHERE battle = %d""" % battle_id
	
	results = {}
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['squad']] = row['losses']
	
	return results

def refund_losses(cursor, battle_id):
	losses = get_all_battle_losses_by_squad(cursor, battle_id)
	
	queries = []
	for s, a in losses.items():
		queries.append("UPDATE squads SET amount = amount + %d WHERE id = %d" % (a, s))
		queries.append("DELETE FROM squad_battle_history WHERE squad = %d AND battle = %d" % (s, battle_id))
	
	database.query(cursor, *queries)

def get_team_losses_from_battle(cursor, team_id, battle_id):
	battles = [str(battle_id)]
	return _get_team_losses(cursor, team_id, battles)

def get_team_losses(cursor, team_id, turn=-1):
	"""Gets all the losses for a turn"""
	if turn == -1:
		turn = common.current_turn()
	
	battles = []
	query = """SELECT b.id
		FROM battles b, campaigns c
			WHERE c.turn = {turn}
			AND b.campaign = c.id""".format(turn=turn)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		battles.append(str(row['id']))
	
	return _get_team_losses(cursor, team_id, battles)

def _get_team_losses(cursor, team_id, battles):
	# No battles? Leave it here then!
	if battles == []: return 0
	total = 0
	query = """SELECT b.losses
		FROM squad_battle_history b, squads s
			WHERE b.squad = s.id
				AND b.battle in (%s)
				AND s.team = %d""" % (",".join(battles), team_id)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		total += row['losses']
	
	return total