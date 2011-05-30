import database
from pages import common
from functions import army_f
from queries import army_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_armies",
}

def main(cursor):
	army_id = int(common.get_val('army', -1))
	the_army = army_q.get_one_army(cursor, army_id)
	database.query(cursor, army_f.make_delete_query(army_id))
	
	# Redirect
	page_data['Redirect'] = 'list_armies&team={0:d}'.format(the_army.team)
