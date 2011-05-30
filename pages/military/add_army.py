import database
import re
from pages import common
from functions import army_f
from queries import city_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_armies",
}

def main(cursor):
	team			= int(common.get_val("team", 0))
	name			= common.get_val("name", 0)
	city_location	= common.get_val("city_location", 0)
	text_location	= common.get_val("text_location", "")
	army_type		= int(common.get_val("type", 0))
	
	actual_x = 0
	actual_y = 0
	
	if text_location != "":
		actual_x = re.search(r"(-?[0-9]+)[,:] ?(-?[0-9]+)", text_location).groups()[0]
		actual_y = re.search(r"(-?[0-9]+)[,:] ?(-?[0-9]+)", text_location).groups()[1]
	else:
		the_city = city_q.get_one_city(city_location)
		
		actual_x = the_city['x']
		actual_y = the_city['y']
	
	database.query(cursor,
		army_f.new_army(name, team, actual_x, actual_y, army_type=army_type))
	
	# Redirect
	page_data['Redirect'] = 'list_armies&team={0:d}'.format(team)
	return ""