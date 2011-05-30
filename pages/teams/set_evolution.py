import database
from pages import common
from functions import team_f
from queries import evolution_q

page_data = {
	"Name":		"set_evolution",
	"Admin":	True,
	"Redirect":	"edit_team",
}

def main(cursor):
	page_data['Redirect'] = ''
	
	evolution		= int(common.get_val("evolution", 0))
	level			= int(common.get_val("evolution_level", 0))
	team_id			= int(common.get_val("team", 0))
	
	current_level = evolution_q.get_one_evolution_level(cursor, evolution, team_id)
	
	# Do we need to save it?
	if level == current_level: return ""
	
	# Cost?
	the_evo = evolution_q.get_one_evolution(cursor, evolution)
	
	diff = level - current_level
	
	# Are we refunding?
	if diff < 0 and current_level > 0:
		if current_level > 0:
			cost = diff * the_evo.cost_per_level/2
	else:
		cost = diff * the_evo.cost_per_level
	
	# if current_level > level and level >= 0:
	# 	cost = ((level - current_level) * the_evo.cost_per_level)/2
	# elif current_level > level and level < 0:
	# 	pos_refund = (current_level * the_evo.cost_per_level)/2
	# 	neg_refund = (-level) * the_evo.cost_per_level
	# 	
	# 	cost = -(pos_refund + neg_refund)
	# else:
	# 	cost = (level - current_level) * the_evo.cost_per_level
	
	# print("")
	# print(cost)
	# exit()
	
	database.query(cursor, team_f.set_evolution(team=team_id, evolution=evolution, level=level, evo_cost=cost))
	
	page_data['Redirect'] = 'edit_team&team={0:d}'.format(team_id)
	return ""