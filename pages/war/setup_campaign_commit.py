from pages import common
from classes import campaign

page_data = {
	"Admin":	True,
	"Redirect":	"setup_campaign",
}

def main(cursor):
	the_campaign = campaign.Campaign()
	the_campaign.get_from_form(common.cgi_form.list)
	the_campaign.update(cursor)
	
	page_data['Redirect'] = "setup_campaign&campaign={0}".format(the_campaign.id)