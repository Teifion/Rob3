import database
from classes import world

def new_campaign(name, turn, sides):
	return """INSERT INTO campaigns (name, turn, sides)
		values
		('%(name)s', %(turn)d, %(sides)d);""" % {
			"name":		database.escape(name),
			"turn":		int(turn),
			"sides":	int(sides),
		}

def add_team_to_campaign(campaign, team, side):
	return """INSERT INTO campaign_teams (campaign, team, side)
		values
		(%(campaign)d, %(team)d, %(side)d);""" % {
			"campaign":	int(campaign),
			"team":		int(team),
			"side":		int(side),
		}


def team_campaign_count(cursor, team_id, turn_min, turn_max=-1):
	"""Returns the number of battles that a team took place in this turn"""
	if turn_max == -1: turn_max = turn_min
	
	query = """SELECT count(*)
		FROM campaign_teams t, campaigns c
			WHERE c.turn >= {turn_min} AND c.turn <= {turn_max}
				AND t.team = {team_id}
				AND c.id = t.campaign""".format(
					turn_min = turn_min,
					turn_max = turn_max,
					team_id = team_id,
			)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['count']

def delete_campaign(campaign_id):
	return [
		"DELETE FROM campaign_teams WHERE campaign = {id}".format(id=campaign_id),
		"DELETE FROM campaign_armies WHERE campaign = {id}".format(id=campaign_id),
		"DELETE FROM battles WHERE campaign = {id}".format(id=campaign_id),
		"DELETE FROM campaigns WHERE id = {id}".format(id=campaign_id),
	]


def remove_team_from_campaign(campaign, side, team):
	return ["DELETE FROM campaign_teams WHERE campaign = %d AND team = %d AND side = %d" % (campaign, team, side)]

def cache_team_losses(cursor = None, the_world = None):
	if the_world == None:
		the_world = world.World(cursor)
	
	

#	Public/Secretness of a team
#------------------------
def make_team_public(team_id, campaign_id):
	return "UPDATE campaign_teams SET secret = False WHERE team = %d AND campaign = %d;" % (team_id, campaign_id)

def make_team_secret(team_id, campaign_id):
	return "UPDATE campaign_teams SET secret = True WHERE team = %d AND campaign = %d;" % (team_id, campaign_id)
