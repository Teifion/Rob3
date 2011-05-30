import database
from pages import common
from functions import power_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_powers",
}

def main(cursor):
	name		= common.get_val("name", "")
	player		= int(common.get_val("player", 0))
	power_type	= int(common.get_val("type", 0))
	description	= common.get_val("power_description", "")
	
	database.query(cursor,
		power_f.new_power(name, player, power_type, description))
	
	# Redirect
	page_data['Redirect'] = 'list_powers'
	return ""