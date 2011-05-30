import database
import re
from pages import common
from functions import city_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_cities",
}

def main(cursor):
	team			= int(common.get_val("team", 0))
	name			= common.get_val("name", "")
	text_location	= common.get_val("text_location", "")
	port			= common.get_val("port", "False")
	secret			= common.get_val("secret", "False")
	dead			= common.get_val("dead", "False")
	nomadic			= common.get_val("nomadic", "False")
	population		= int(common.get_val("population", "0").replace(',', ''))
	slaves			= int(common.get_val("slaves", "0").replace(',', ''))
	
	actual_x = 0
	actual_y = 0
	
	if text_location != "":
		actual_x = re.search(r"(-?[0-9]*)[,:] ?(-?[0-9]*)", text_location).groups()[0]
		actual_y = re.search(r"(-?[0-9]*)[,:] ?(-?[0-9]*)", text_location).groups()[1]
	
	database.query(cursor,
		city_f.new_city(name, team, actual_x, actual_y, port, secret, dead, nomadic, population, slaves))
	
	# Redirect
	page_data['Redirect'] = 'list_cities&team={0:d}'.format(team)
	return ""