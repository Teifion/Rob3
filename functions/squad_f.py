import database
from queries import squad_q
from functions import battle_f

def new_squad(name, army, unit, amount=0, team=-1, experience=0):
	"""Adds a new squad to an army, easy peasy"""
	
	if team < 1:
		raise Exception("No team declared")
	
	query = """INSERT INTO squads (name, army, unit, team, amount, experience)
		values
		('%(name)s', %(army)d, %(unit)d, %(team)d, %(amount)d, %(experience)d);""" % {
			"name":	database.escape(name),
			"army":			army,
			"unit":			unit,
			"amount":		amount,
			"team":			team,
			"experience":	experience,
		}
	
	return query

def apply_losses_to_squads(cursor, amount, squad_list, battle_id):
	"""Send a list of squad IDs, losses will be applied to them"""
	squad_dict		= squad_q.get_squads_from_list(cursor, squad_list)
	amount_left		= amount
	
	if amount < 0:
		amount_per_squad = int(amount/float(len(squad_list)))
		amount_left_over = amount % len(squad_list)
		
		amount_per_squad = -amount_per_squad
		amount_left_over = -amount_left_over
		
		for s in squad_list:
			# print (amount_per_squad - amount_left_over), "<br />"
			battle_f.remove_loss(cursor, amount_per_squad - amount_left_over, s, battle_id)
			amount_left_over = 0
	else:
		for s in squad_list:
			if amount_left <= 0: return 0
			
			# If the squad has more in it than there is left to remove, remove all of it
			if squad_dict[s].amount > amount_left:
				battle_f.add_loss(cursor, amount_left, s, battle_id)
				amount_left = 0
			else:
				amount_left -= squad_dict[s].amount
				battle_f.add_loss(cursor, squad_dict[s].amount, s, battle_id)
	
	return amount_left

def make_reinforcement_query(squad_id, amount):
	return ["""UPDATE squads SET amount = amount+%d WHERE id = %d;""" % (int(amount), int(squad_id))]

def make_squad_move_query(squad_id, new_army):
	return ["UPDATE squads SET army = '%d' WHERE id = %d;" % (int(new_army), int(squad_id))]

def make_delete_query(squad_id):
	return [
		"DELETE FROM squad_battle_history WHERE squad = %d;" % int(squad_id),
		"DELETE FROM squads WHERE id = %d;" % int(squad_id),
	]

def make_disband_query(squad_id, amount=-1):
	if amount < 1:
		return ["""UPDATE squads SET amount = 0 WHERE id = %d;""" % (int(squad_id))]
	else:
		return ["""UPDATE squads SET amount = amount-%d WHERE id = %d;""" % (int(amount), int(squad_id))]

def make_rename_query(squad_id, new_name):
	return ["UPDATE squads SET name = '%s' WHERE id = %d;" % (database.escape(new_name), squad_id)]

def make_split_queries(squad_1, squad_2, amount):
	queries = ["""UPDATE squads SET amount = amount+%d WHERE id = %d;""" % (int(amount), int(squad_2)),
	"""UPDATE squads SET amount = amount-%d WHERE id = %d;""" % (int(amount), int(squad_1))]
	return queries

