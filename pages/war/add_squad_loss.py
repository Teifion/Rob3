# Adds losses to this squad from this battle

import database
from pages import common
from queries import battle_q, squad_q
from functions import squad_f

page_data = {
	"Admin":	True,
	"Redirect":	"setup_campaign",
}

def main(cursor):
	battle_id	= int(common.get_val("battle", -1))
	squad_id	= int(common.get_val("squad", -1))
	amount		= int(common.get_val("amount", 0))
	
	if battle_id < 1:
		raise Exception("No battle supplied")
	
	if squad_id < 1:
		raise Exception("No team/unit supplied")
	
	if amount == 0:
		return ""
		raise Exception("No amount supplied")
	
	if amount < 0:
		return refund_losses(cursor, battle_id, squad_id, -amount)
	
	# return str(squad_list)
	squad_f.apply_losses_to_squads(cursor, amount, [squad_id], battle_id)
	return ""

def refund_losses(cursor, battle_id, squad_id, amount):
	# Get all handles and instances
	losses		= battle_q.get_all_battle_losses_by_squad(cursor, battle_id)
	# the_squad	= squad_q.get_one_squad(cursor, squad_id)
	
	queries = []
	actual_losses = min(amount, losses.get(squad_id, 0))
	
	queries.append("UPDATE squads SET amount = amount + %d WHERE id = %d;" % (actual_losses, squad_id))
	queries.append("UPDATE squad_battle_history SET losses = losses - %d WHERE squad = %d AND battle = %d;" % (actual_losses, squad_id, battle_id))
	
	# print(queries)
	# exit()
	
	database.query(cursor, *queries)
	return ""