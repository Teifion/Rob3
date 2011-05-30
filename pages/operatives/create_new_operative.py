import database
from pages import common
from functions import operative_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_operatives",
}

def main(cursor):
	city			= int(common.get_val("city"))
	team			= int(common.get_val("team"))
	arrival			= int(common.get_val("arrival"))
	size			= int(common.get_val("size"))
	stealth			= int(common.get_val("stealth"))
	observation		= int(common.get_val("observation"))
	integration		= int(common.get_val("integration"))
	sedition		= int(common.get_val("sedition"))
	sabotage		= int(common.get_val("sabotage"))
	assassination	= int(common.get_val("assassination"))
	name		= common.get_val("name", "")
	
	database.query(cursor,
		operative_f.new_operative(city, team, arrival, size, stealth, observation, integration, sedition, sabotage, assassination, name))
	
	# Redirect
	page_data['Redirect'] = 'list_operatives&team={0:d}'.format(team)
	return ""
