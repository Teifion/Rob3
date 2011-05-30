from pages import common
from classes import artefact
from queries import city_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_artefacts",
}

def main(cursor):
	# Artefact settings
	the_artefact = artefact.Artefact()
	the_artefact.get_from_form(common.cgi_form.list)
	
	# Set the team based on the city
	the_city = city_q.get_one_city(cursor, the_artefact.city)
	the_artefact.team = the_city.team
	
	the_artefact.update(cursor)
	
	# Redirect
	page_data['Redirect'] = "list_artefacts&team={0}".format(the_artefact.team)
	return ""