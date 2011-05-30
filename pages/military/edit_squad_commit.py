from pages import common
from classes import squad

page_data = {
	"Admin":	True,
	"Redirect":	"list_units",
}

def main(cursor):
	the_squad = squad.Squad()
	the_squad.get_from_form(common.cgi_form.list)
	the_squad.update(cursor)
	
	page_data['Redirect'] = "list_squads&army={0}".format(the_squad.army)
	return ""