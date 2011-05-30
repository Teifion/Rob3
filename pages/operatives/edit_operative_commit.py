from pages import common
from classes import operative

page_data = {
	"Admin":	True,
	"Redirect":	"list_cities",
}

def main(cursor):
	the_operative = operative.Operative()
	the_operative.get_from_form(common.cgi_form.list)
	the_operative.update(cursor)
	
	page_data['Redirect'] = "list_operatives&team={0}".format(the_operative.team)
	return ""