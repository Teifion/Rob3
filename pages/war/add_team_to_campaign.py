import database
from pages import common
from functions import campaign_f

page_data = {
	"Admin":	True,
	"Redirect":	"",
}

def main(cursor):
	campaign	= int(common.get_val("campaign"))
	side		= int(common.get_val("side"))
	team		= int(common.get_val("team"))
	
	try:
		database.query(cursor,
			campaign_f.add_team_to_campaign(campaign, team, side))
	except Exception as e:
		# It's expected to fail if the team is already on that side
		pass
	
	return ""