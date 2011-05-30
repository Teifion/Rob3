import database
from pages import common
from functions import campaign_f
from queries import campaign_q, army_q, squad_q, battle_q

page_data = {
	"Admin":	True,
	"Redirect":	"edit_campaign",
}

def main(cursor):
	army_ids	= common.get_val('army_ids').split(",")
	campaign_id = int(common.get_val('campaign'))
	
	add_list		= []
	remove_list		= []
	
	# Get campaign
	the_campaign = campaign_q.get_one_campaign(cursor, campaign_id)
	the_campaign.get_armies_basic(cursor)
	
	# Get last battle
	last_battle = battle_q.get_last_battle_from_campaign(cursor, campaign_id)
	if not last_battle:
		page_data['Redirect'] = 'setup_campaign&campaign=%d' % campaign_id
		return ""
	
	start_time = last_battle.start
	
	# Amies dict
	army_dict = army_q.get_all_armies(cursor)
	
	for a in army_ids:
		i = common.get_val('a_%s' % a, 'False')
		if i == 'False':
			# Remove it
			if int(a) in the_campaign.armies_basic:
				remove_list.append(a)
		
		elif i == 'True':
			# Add it
			if int(a) not in the_campaign.armies_basic:
				add_list.append("(%d, %s, %d)" % (campaign_id, a, start_time))
	
	if remove_list != []:
		database.query(cursor, "DELETE FROM campaign_armies WHERE army in (%s)" % ",".join(remove_list))
	
	if add_list != []:
		database.query(cursor, "INSERT INTO campaign_armies (campaign, army, started) values %s;" % ",".join(add_list))
	
	page_data['Redirect'] = 'setup_campaign&campaign=%d' % campaign_id
	return ""
