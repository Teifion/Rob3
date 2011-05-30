import database
from pages import common
from functions import squad_f
from queries import squad_q

page_data = {
	"Admin":	True,
	"Redirect":	"edit_army",
}

def main(cursor):
	squad_id = int(common.get_val('squad', -1))
	the_squad = squad_q.get_one_squad(cursor, squad_id)
	database.query(cursor, squad_f.make_delete_query(squad_id))
	
	# Redirect
	page_data['Redirect'] = 'edit_army&army={0:d}'.format(the_squad.army)