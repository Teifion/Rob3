import database
from pages import common
from classes import squad
from functions import monster_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_units",
}

def main(cursor):
	monster_id	= int(common.get_val('monster', 0))
	army_id 	= int(common.get_val('army', 0))
	amount  	= int(common.get_val('amount', 0))
	
	database.query(cursor, monster_f.alter_army_monster_size(army_id, monster_id, amount))
	
	page_data['Redirect'] = "list_squads&army={0}".format(army_id)
	return ""