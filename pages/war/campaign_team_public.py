import database
from pages import common
from functions import campaign_f

page_data = {
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	team		= int(common.get_val('team', 0))
	campaign	= int(common.get_val('campaign', 0))
	
	database.query(cursor, campaign_f.make_team_public(team, campaign))
	return ""