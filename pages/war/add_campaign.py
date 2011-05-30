import database
from pages import common
from functions import campaign_f
from queries import campaign_q

page_data = {
	"Admin":	True,
	"Redirect":	"setup_campaign",
}

def main(cursor):
	name	= common.get_val("name", "")
	turn	= int(common.get_val("turn", 0))
	sides	= int(common.get_val("sides", 2))
	
	# Insert
	database.query(cursor,
		campaign_f.new_campaign(name, turn, sides))
	
	# Get latest
	new_campaign = campaign_q.get_latest_campaign(cursor)
	
	# Redirect
	# page_data['Redirect'] = 'setup_campaign&campaign={0:d}'.format(new_campaign.id)
	page_data['Redirect'] = 'list_battles&campaign={0:d}'.format(new_campaign.id)