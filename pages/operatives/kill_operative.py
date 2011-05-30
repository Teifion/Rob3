import database
from pages import common
from functions import operative_f
from queries import operative_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_operatives",
}

def main(cursor):
	op_id = int(common.get_val('operative', -1))
	the_op = operative_q.get_one_operative(cursor, op_id)
	database.query(cursor, operative_f.kill_operative(op_id))
	
	# Redirect
	page_data['Redirect'] = 'list_operatives&team={0:d}'.format(the_op.team)
