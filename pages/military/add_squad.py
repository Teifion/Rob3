import database
from pages import common
from functions import squad_f

# from data import squad_f
# from data import squad_q

page_data = {
	"Admin":	True,
	"Redirect":	"edit_army",
}

def main(cursor):
	team		= int(common.get_val("team", -1))
	name		= common.get_val("name", "")
	army_id		= int(common.get_val("army", 0))
	unit_type	= int(common.get_val("unit_type", 0))
	experience	= int(common.get_val("experience", 0))
	amount		= int(common.get_val("size", 0))
	
	database.query(cursor,
		squad_f.new_squad(name, army_id, unit_type, amount=amount, team=team, experience=experience))
	
	# Redirect
	page_data['Redirect'] = 'edit_army&army={0:d}'.format(army_id)
	return ""