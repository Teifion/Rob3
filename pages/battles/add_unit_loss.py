# Adds losses to all units of that type in this battle, covers many squads

import database
from pages import common
from data import team, team_q
from data import battle, battle_q
from data import squad, squad_f

battle_id	= int(common.get_val("battle", -1))
team_id		= int(common.get_val("team", -1))
unit_id		= int(common.get_val("unit", -1))
amount		= int(common.get_val("amount", 0))

if battle_id < 1:
	print "location:list_battles"
	exit()

if team_id < 1 or unit_id < 1 or amount == 0:
	print "location:view_battle&battle=%s" % battle_id
	exit()

# Get all handles and instances
the_battle		= battle.Battle(battle_q.get_one_battle(battle_id))
squads			= the_battle.get_squads()
the_team		= team.Team(team_q.get_one_team(team_id))
squad_dict_c	= squad.get_squad_dict_c()

squad_list = []

for s, a in squads.items():
	the_squad = squad_dict_c[s]
	if the_squad.team != team_id or the_squad.unit != unit_id: continue
	squad_list.append(s)

squad_f.apply_losses_to_squads(amount, squad_list, battle_id)

# print database.cursor.query_list
# print "Done"

# Redirect
# print "location:view_battle&battle=%s" % battle_id