import database
from pages import common
from queries import operative_q
from functions import operative_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_operatives",
}

def main(cursor):
	operative_id = int(common.get_val('operative', -1))
	the_operative = operative_q.get_one_operative(cursor, operative_id)
	database.query(cursor, operative_f.delete_operative(operative_id))
	
	# Redirect
	page_data['Redirect'] = 'list_operatives&team={0:d}'.format(the_operative.team)