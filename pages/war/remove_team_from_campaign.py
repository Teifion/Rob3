import database
from pages import common
from functions import campaign_f

page_data = {
	"Admin":	True,
	"Redirect":	"",
}

def main(cursor):
	campaign	= int(common.get_val("campaign"))
	team		= int(common.get_val("team"))
	side		= int(common.get_val("side"))
	
	database.query(cursor,
		campaign_f.remove_team_from_campaign(campaign, side, team))
	
	return ""