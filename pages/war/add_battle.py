import database
from pages import common
from queries import battle_q, city_q
from functions import battle_f
from classes import battle
from functions import path_f
import math

page_data = {
	"Admin":	True,
	"Redirect":	"list_battles",
}

def main(cursor):
	name		= common.get_val("name", "")
	campaign	= int(common.get_val("campaign", 0))
	start		= int(common.get_val("start", 0))
	duration	= int(common.get_val("duration", 0))
	btype		= int(common.get_val("type", 0))
	location	= common.get_val("location", "")
	city		= int(common.get_val("city", 0))
	
	# Get location
	result = battle.battle_coords.search(location)
	if result != None:
		x = int(result.groups()[0])
		y = int(result.groups()[1])
	else:
		if city > 0:
			the_city = city_q.get_one_city(cursor, city)
			x, y = the_city.x, the_city.y
		else:
			x, y = 0, 0
	
	# If no name is supplied then it may be from a city
	if name == '':
		if city > 0:
			name = the_city.name
		else:
			page_data['Redirect'] = 'setup_campaign&campaign={0}'.format(campaign)
			return ""
	
	# If there is no last battle then we can't use auto pather to work out start time
	last_battle = battle_q.get_last_battle_from_campaign(cursor, campaign)
	if start < 0 and last_battle == None:
		start = 0
	
	# If negative start time then work out travel time
	if start < 0:
		waypoints = ((last_battle.x, last_battle.y), (x, y))
		b_path = path_f.path(cursor, waypoints, move_speed="Marching", move_type="Medium foot")
		start = math.ceil(b_path.time_cost) + last_battle.start + last_battle.duration
	
	database.query(cursor,
		battle_f.new_battle(name, campaign, start, duration, x, y, btype=btype, city=city))
	
	# page_data['Redirect'] = 'list_battles&campaign={0}'.format(campaign)
	page_data['Redirect'] = 'setup_campaign&campaign={0}'.format(campaign)
	return ""