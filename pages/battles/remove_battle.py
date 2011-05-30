import database
from pages import common
from functions import battle_f
from queries import battle_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_battles",
}

def main(cursor):
	battle_id = int(common.get_val('battle', -1))
	the_battle = battle_q.get_one_battle(cursor, battle_id)
	database.query(cursor, battle_f.make_delete_query(battle_id))
	
	# Redirect
	page_data['Redirect'] = 'list_battles&campaign={0:d}'.format(the_battle.campaign)
