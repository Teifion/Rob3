from pages import common
from classes import army

page_data = {
	"Admin":	True,
	"Redirect":	"list_armies",
}

def main(cursor):
	the_army = army.Army()
	the_army.get_from_form(common.cgi_form.list)
	the_army.update(cursor)
	
	page_data['Redirect'] = "list_armies&team={0}".format(the_army.team)
	return ""