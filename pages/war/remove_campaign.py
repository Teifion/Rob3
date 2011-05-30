import database
from pages import common
from functions import campaign_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_campaigns",
}

def main(cursor):
	campaign_id = int(common.get_val('campaign', -1))
	database.query(cursor, campaign_f.delete_campaign(campaign_id))
