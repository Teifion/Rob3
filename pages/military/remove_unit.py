import database
from pages import common
from functions import unit_f
from queries import unit_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_cities",
}

def main(cursor):
	unit_id = int(common.get_val('unit', -1))
	the_unit = unit_q.get_one_unit(cursor, unit_id)
	database.query(cursor, unit_f.delete_unit(unit_id))
	
	# Redirect
	page_data['Redirect'] = 'list_units&team={0:d}'.format(the_unit.team)
