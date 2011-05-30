import database
from pages import common
from functions import team_f

page_data = {
	"Admin":	True,
	"Redirect":	"edit_team",
}

def main(cursor):
	page_data['Redirect'] = ''
	
	trait_id	= int(common.get_val("trait", 0))
	team_id		= int(common.get_val("team", 0))
	
	database.query(cursor, team_f.add_trait(team_id, trait_id))
	
	page_data['Redirect'] = 'edit_team&team={0:d}'.format(team_id)
	return ""