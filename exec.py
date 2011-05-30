#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3

print("Content-type: text/html")

import database
import cgitb
cgitb.enable()

from pages import common
from pages import headers

common.data['mode'] = common.get_val('mode', '')
m = common.data['mode']

# print("")
# print(common.print_post_data())
# exit()

class HTTP404 (object):
	page_data = {
		'Title':	"HTTP 404",
	}
	def __init__(self):
		super(HTTP404, self).__init__()
	
	def main(self, *args, **kwargs):
		return "404 for '%s'\n\n%s" % (common.get_val('mode'), common.print_post_data())

# Teams
if m == 'edit_team_commit':	import pages.teams.edit_team_commit as the_page
 
elif m == 'edit_borders':		import pages.teams.edit_borders as the_page
elif m == 'set_evolution':		import pages.teams.set_evolution as the_page
elif m == 'add_deity':			import pages.teams.add_deity as the_page
elif m == 'remove_deity':		import pages.teams.remove_deity as the_page

# Battles
elif m == 'remove_battle':			import pages.battles.remove_battle as the_page
# elif m == 'add_battle':				import pages.battles.add_battle as the_page
elif m == 'edit_battle_commit':		import pages.battles.edit_battle_commit as the_page
# elif m == 'add_team_battle':			import pages.battles.add_team_battle as the_page
# elif m == 'remove_team_battle':		import pages.battles.remove_team_battle as the_page

elif m == 'mass_add_armies':			import pages.war.mass_add_armies as the_page
elif m == 'move_armies':				import pages.war.move_armies as the_page
# elif m == 'remove_army_from_battle':	import pages.battles.remove_army_from_battle as the_page

# Espionage
# elif m == 'add_report':				import pages.mission.add_report as the_page
# elif m == 'edit_report_commit':		import pages.mission.edit_report_commit as the_page
# elif m == 'delete_report':			import pages.mission.delete_report as the_page

# Campaigns
elif m == 'add_campaign':				import pages.war.add_campaign as the_page
elif m == 'add_battle':					import pages.war.add_battle as the_page
elif m == 'setup_campaign_commit':		import pages.war.setup_campaign_commit as the_page

elif m == 'add_team_to_campaign':		import pages.war.add_team_to_campaign as the_page
elif m == 'remove_team_from_campaign':	import pages.war.remove_team_from_campaign as the_page
elif m == 'edit_campaign_armies':		import pages.war.edit_campaign_armies as the_page
elif m == 'remove_campaign':			import pages.war.remove_campaign as the_page

# Military
elif m == 'edit_army_commit':		import pages.military.edit_army_commit as the_page
elif m == 'edit_squad_commit':		import pages.military.edit_squad_commit as the_page
elif m == 'edit_unit_commit':		import pages.military.edit_unit_commit as the_page
elif m == 'edit_army_monster_commit':	import pages.military.edit_army_monster_commit as the_page

elif m == 'remove_equipment':		import pages.military.remove_equipment as the_page
elif m == 'add_equipment':			import pages.military.add_equipment as the_page
elif m == 'alter_unit_count':		import pages.military.alter_unit_count as the_page

elif m == 'add_units_to_army':		import pages.military.add_units_to_army as the_page
elif m == 'add_units_to_squad':		import pages.military.add_units_to_squad as the_page
elif m == 'add_squad_to_army':		import pages.military.add_squad_to_army as the_page
elif m == 'add_army':				import pages.military.add_army as the_page
elif m == 'add_squad':				import pages.military.add_squad as the_page

elif m == 'remove_army':				import pages.military.remove_army as the_page
elif m == 'remove_squad':			import pages.military.remove_squad as the_page
elif m == 'remove_unit':				import pages.military.remove_unit as the_page

elif m == 'create_new_unit':			import pages.military.create_new_unit as the_page

# Missions
# elif m == 'edit_mission_commit':		import pages.mission.edit_mission_commit as the_page
# elif m == 'remove_mission':			import pages.mission.remove_mission as the_page
# elif m == 'add_mission':				import pages.mission.add_mission as the_page
# elif m == 'handle_mission_commit':	import pages.mission.handle_mission_commit as the_page

# Operatives
elif m == 'create_new_operative':	import pages.operatives.create_new_operative as the_page
elif m == 'edit_operative_commit':	import pages.operatives.edit_operative_commit as the_page
elif m == 'remove_operative':		import pages.operatives.remove_operative as the_page
elif m == 'kill_operative':			import pages.operatives.kill_operative as the_page
elif m == 'revive_operative':		import pages.operatives.revive_operative as the_page

# Players
elif m == 'add_power':				import pages.players.add_power as the_page
elif m == 'edit_power_commit':		import pages.players.edit_power_commit as the_page
elif m == 'edit_feat_commit':		import pages.players.edit_feat_commit as the_page

elif m == 'add_kill':				import pages.players.add_kill as the_page
elif m == 'remove_kill':			import pages.players.remove_kill as the_page

elif m == 'edit_player_commit':		import pages.players.edit_player_commit as the_page

# Artefacts
elif m == 'add_artefact':			import pages.artefacts.add_artefact as the_page
elif m == 'edit_artefact_commit':	import pages.artefacts.edit_artefact_commit as the_page

# Traits
elif m == 'add_trait':				import pages.teams.add_trait as the_page
elif m == 'remove_trait':			import pages.teams.remove_trait as the_page

# Research
elif m == 'set_spell':				import pages.research.set_spell as the_page
elif m == 'set_tech':				import pages.research.set_tech as the_page

# Cities
elif m == 'edit_city_commit':	import pages.cities.edit_city_commit as the_page
elif m == 'set_building':		import pages.cities.set_building as the_page
elif m == 'add_city':			import pages.cities.add_city as the_page
elif m == 'remove_city':		import pages.cities.remove_city as the_page

elif m == 'add_wonder':				import pages.cities.add_wonder as the_page
elif m == 'edit_wonder_commit':		import pages.cities.edit_wonder_commit as the_page
elif m == 'remove_wonder':			import pages.cities.remove_wonder as the_page

# Map
# elif m == 'add_continent':			import pages.map.add_continent as the_page

# Nothing? 404?
else:								the_page = HTTP404()


output = []

cursor = database.get_cursor()
page_results = the_page.main(cursor)
ajax = bool(common.get_val('ajax', False))

if the_page.page_data.get("Redirect", "") != "":
	print("Location: web.py?mode={0}".format(the_page.page_data["Redirect"]))
	print("")

else:
	if the_page.page_data.get("Header", True) and page_results != "" and ajax != True:
		output.append(headers.main(cursor, the_page.page_data))
	
	output.append(page_results)
	
	if the_page.page_data.get("Header", True) and page_results != "" and ajax != True:
		output.append(headers.footers(cursor))
	
	print("")
	print(common.de_unicode("".join(output)))