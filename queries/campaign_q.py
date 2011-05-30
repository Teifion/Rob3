import database
import collections
from classes import campaign
from queries import battle_q
from pages import common

def _campaign_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM campaigns"
	
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
		results[row['id']] = campaign.Campaign(row)
	
	return results

def get_all_campaigns(cursor):
	return _campaign_query(cursor)

def get_campaigns_from_turn(cursor, turn):
	return _campaign_query(cursor, where = "turn = %d" % (int(turn)))

def get_latest_campaign(cursor):
	return _campaign_query(cursor, orderby="id DESC", limit=1).popitem()[1]

def get_one_campaign(cursor, the_campaign):
	if type(the_campaign) == str:
		query = "SELECT * FROM campaigns WHERE name = '{0:s}' ORDER BY id DESC LIMIT 1;".format(database.escape(the_campaign))
	else:
		query = "SELECT * FROM campaigns WHERE id = {0:d} LIMIT 1;".format(int(the_campaign))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return campaign.Campaign(row)

def get_campaign_armies_from_turn(cursor, turn=-1):
	if turn < 1: turn = common.current_turn()
	
	army_turns = {}
	query = """SELECT a.campaign, a.army
		FROM campaign_armies a, campaigns c
			WHERE c.turn = {t} AND c.id = a.campaign""".format(t=turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['army'] not in army_turns:
			army_turns[row['army']] = []
		
		army_turns[row['army']].append(row['campaign'])
	return army_turns

def get_armies_from_campaign_from_team(cursor, campaign, team):
	armies = []
	
	query = """SELECT a.id
		FROM campaign_armies c, armies a
			WHERE a.team = {t} AND c.army = a.id AND c.campaign = {c}""".format(t=team, c=campaign)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		armies.append(row['id'])
	
	return armies

def get_campaigns_from_team(cursor, team_id, include_secret=False, since_turn=0):
	"""Returns an ID list of the campaigns for this team, in order of date"""
	# Since which turn?
	if since_turn > 1:
		turn_where = "AND c.turn >= %d" % since_turn
	else:
		turn_where = ""
	
	# Include secret teams in this list?
	if include_secret:
		secret_where = ""
	else:
		secret_where = "AND t.secret = False"
	
	query = """SELECT t.campaign
		FROM campaigns c, campaign_teams t
			WHERE t.team = %d
			AND c.id = t.campaign
			%s %s""" % (team_id, turn_where, secret_where)
	
	campaign_list = []
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		campaign_list.append(str(row['campaign']))
	if campaign_list == []: return {}
	
	return _campaign_query(cursor, where="id in (%s)" % ",".join(campaign_list), orderby="turn DESC, name")

def get_all_losses(cursor, campaign_id):
	losses = {}
	# Get teams from campaign
	query = """SELECT team FROM campaign_teams WHERE campaign = {0}""".format(campaign_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		losses[row['team']] = 0
	
	for t in losses.keys():
		losses[t] = get_team_losses(cursor, t, campaign_id)
	
	return losses

def get_team_losses(cursor, team_id, campaign_id):
	# Get battle list
	battles = []
	query = """SELECT id FROM battles WHERE campaign = {0}""".format(campaign_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		battles.append(str(row['id']))
	
	return battle_q._get_team_losses(cursor, team_id, battles)

def mass_get_campaign_teams(cursor, campaign_dict):
	for k, the_campaign in campaign_dict.items():
		the_campaign.teams = []
	
	query = "SELECT campaign, team FROM campaign_teams"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['campaign'] not in campaign_dict: continue
		campaign_dict[row['campaign']].teams.append(row['team'])
	
	return campaign_dict