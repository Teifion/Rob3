from pages import common
from classes import unit

page_data = {
	"Admin":	True,
	"Redirect":	"list_units",
}

def main(cursor):
	the_unit = unit.Unit()
	the_unit.get_from_form(common.cgi_form.list)
	the_unit.update(cursor)
	
	page_data['Redirect'] = "list_units&team={0}".format(the_unit.team)
	return ""