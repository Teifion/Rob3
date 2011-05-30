from pages import common
from classes import city

page_data = {
	"Admin":	True,
	"Redirect":	"list_cities",
}

def main(cursor):
	the_city = city.City()
	the_city.get_from_form(common.cgi_form.list)
	the_city.update(cursor)
	
	# Redirect
	page_data['Redirect'] = "list_cities&team={0}".format(the_city.team)
	return ""