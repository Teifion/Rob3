from pages import common
from classes import battle

page_data = {
	"Admin":	True,
	"Redirect":	"list_battles",
}

def main(cursor):
	# battle settings
	the_battle = battle.Battle()
	the_battle.get_from_form(common.cgi_form.list)
	the_battle.update(cursor)
	
	# Redirect
	page_data['Redirect'] = "list_battles&campaign={0}".format(the_battle.campaign)
	return ""