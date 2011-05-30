import database
from queries import building_q

def check_row_exists(army_id, monster_id):
	# print("INSERT INTO army_monsters (army, monster) values (%d, %d);" % (army_id, monster_id))
	return ["INSERT INTO army_monsters (army, monster) values (%d, %d);" % (army_id, monster_id)]

def alter_army_monster_size(army_id, monster_id, amount):
	return [
		"DELETE FROM army_monsters WHERE army = %d AND monster = %d" % (army_id, monster_id),
		"INSERT INTO army_monsters (army, monster, amount) values (%d, %d, %d);" % (army_id, monster_id, amount),
	]