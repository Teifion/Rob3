import database
from pages import common
from functions import player_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_players",
}

def main(cursor):
	player_id	= int(common.get_val("player", 0))
	killer		= int(common.get_val("killer", 0))
	victim		= int(common.get_val("victim", 0))
	battle		= int(common.get_val("battle", -1))
	turn		= int(common.get_val("turn", 0))
	
	database.query(cursor,
		player_f.add_kill(killer, victim, turn=turn, battle=battle)
	)
	
	if battle > 0:
		page_data['Redirect'] = "list_battles&battle=%d" % battle
	
	if player_id > 0:
		page_data['Redirect'] = "edit_player&player=%d" % player_id
	
	return ""