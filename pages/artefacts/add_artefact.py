import database
from pages import common
from functions import artefact_f

page_data = {
	"Admin":	True,
	"Redirect":	"edit_team",
}

def main(cursor):
	team			= int(common.get_val("team", 0))
	name			= common.get_val("name", "")
	location		= int(common.get_val("location", 0))
	description		= common.get_val("artefact_description", "")
	
	database.query(cursor,
		artefact_f.new_artefact(name, team, location, description))
	
	# Redirect
	if team < 1:
		page_data['Redirect'] = 'list_artefacts'
	else:
		page_data['Redirect'] = 'list_artefacts&team={0:d}'.format(team)
	
	return ""