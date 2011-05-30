import database
from pages import common
from functions import campaign_f
from queries import campaign_q, army_q, battle_q

page_data = {
	"Admin":	True,
	"Redirect":	"setup_campaign",
}

def main(cursor):
	campaign_id = int(common.get_val('campaign', -1))
	team_id = int(common.get_val('team', -1))
	army_names_normal = common.get_val('army_names', "").replace("\n", ",").split(",")
	
	# Get last battle
	last_battle = battle_q.get_last_battle_from_campaign(cursor, campaign_id)
	if not last_battle:
		page_data['Redirect'] = 'setup_campaign&campaign=%d' % campaign_id
		return ""
	
	start_time = last_battle.start
	
	army_names = []
	for a in army_names_normal:
		army_names.append(a.lower().strip())
	
	army_dict = army_q.get_armies_from_team(cursor, team_id, True)
	army_list = []
	
	queries = []
	for army_id, the_army in army_dict.items():
		if the_army.name.lower() in army_names:
			queries.append("INSERT INTO campaign_armies (campaign, army, started) values (%d, %d, %d);" % (campaign_id, army_id, start_time))
	
	# print("")
	# print([a.name.lower() for i, a in army_dict.items()], "<br />")
	# print(army_names)
	# print("<br />".join(queries))
	# exit()
	
	# print("")
	# print(queries)
	# exit()
	
	for q in queries:
		try:
			cursor.execute(q)
		except Exception as e:
			pass
			# raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), q))
	
	# if queries == []:
	# 	print("")
	# 	print(army_names)
	# 	
	# 	exit()
	
	# Redirect
	page_data['Redirect'] = 'setup_campaign&campaign={0:d}'.format(campaign_id)


"""
HIMS Lohengramm, 1st Fleet
2nd Fleet
3rd Fleet
Horse Transports
Air Fleet
4th Army
5th Army
6th Army
7th Army
8th Army
Sacred Army
Imperial Guard
War Machines
"""