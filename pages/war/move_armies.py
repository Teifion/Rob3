import database
from pages import common
from functions import army_f
from classes import battle
from queries import battle_q, campaign_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_battles",
}

def main(cursor):
	campaign	= int(common.get_val("campaign", 0))
	location	= common.get_val("location", "")
	team		= int(common.get_val("team", 0))
	
	# Get location
	result = battle.battle_coords.search(location)
	if result != None:
		x = int(result.groups()[0])
		y = int(result.groups()[1])
	else:
		# Get it from the last battle
		last_battle = battle_q.get_last_battle_from_campaign(cursor, campaign)
		if last_battle == None: return ""
		
		x = last_battle.x
		y = last_battle.y
	
	# Get armies
	armies = campaign_q.get_armies_from_campaign_from_team(cursor, campaign, team)	
	
	# Move them
	database.query(cursor,
		army_f.move_armies(armies, (x, y)))
	
	page_data['Redirect'] = "list_battles&campaign={0}".format(campaign)
	return ""