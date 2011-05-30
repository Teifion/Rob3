# Adds losses to all units of that type in this battle, covers many squads

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
	team_id		= int(common.get_val("team", -1))
	unit_id		= int(common.get_val("unit", -1))
	amount		= int(common.get_val("amount", 0))
	
	if battle_id < 1:
		raise Exception("No battle supplied")
	
	if team_id < 1 or unit_id < 1:
		raise Exception("No team/unit supplied")
	
	if amount == 0:
		return ""
		raise Exception("No amount supplied")
	
	if amount < 0:
		return refund_losses(cursor, battle_id, team_id, unit_id, amount)
	
	# Get all handles and instances
	the_battle		= battle_q.get_one_battle(cursor, battle_id)
	battle_squads	= the_battle.get_squads(cursor)
	squad_dict		= squad_q.get_squads_of_type(cursor, unit_id, team_id)
	
	squad_list = [s for s in battle_squads if s in squad_dict]
	
	# return str(squad_list)
	squad_f.apply_losses_to_squads(cursor, amount, squad_list, battle_id)
	return ""

def refund_losses(cursor, battle_id, team_id, unit_id, amount):
	# Get all handles and instances
	the_battle		= battle_q.get_one_battle(cursor, battle_id)
	losses			= battle_q.get_all_battle_losses_by_squad(cursor, battle_id)
	squad_dict		= squad_q.get_squads_of_type(cursor, unit_id, team_id)
	
	queries = []
	temp_amount = -amount
	for s, actual_amount in losses.items():
		if s in squad_dict and squad_dict[s].unit == unit_id:
			a = min(temp_amount, actual_amount)
			temp_amount -= a
			
			queries.append("UPDATE squads SET amount = amount + %d WHERE id = %d;" % (a, s))
			queries.append("UPDATE squad_battle_history SET losses = losses - %d WHERE squad = %d AND battle = %d;" % (a, s, battle_id))
	
	database.query(cursor, *queries)
	return ""