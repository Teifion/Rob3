import database
from pages import common
from functions import team_f

page_data = {
	"Admin":	True,
	"Redirect":	"edit_team",
}

def main(cursor):
	page_data['Redirect'] = ''
	
	deity_id	= int(common.get_val("deity", 0))
	team_id		= int(common.get_val("team", 0))
	
	database.query(cursor, team_f.add_deity(team_id, deity_id))
	
	page_data['Redirect'] = 'edit_team&team={0:d}'.format(team_id)
	return ""