#!/usr/bin/env python

import os
import database

from queries import sync_q
from functions import sync_f

from classes import army
from classes import artefact
from classes import battle
from classes import campaign
from classes import city
from classes import intorder
from classes import log
from classes import mapper
from classes import mission
from classes import operative
from classes import order_post
from classes import player
from classes import power
from classes import queries
from classes import results
from classes import spy_report
from classes import squad
from classes import stat
from classes import team
from classes import turn
from classes import unit
from classes import wonder

from data_classes import building
from data_classes import deity
from data_classes import equipment
from data_classes import evolution
from data_classes import monster
from data_classes import servant
from data_classes import spell
from data_classes import tech
from data_classes import trait
from data_classes import lore_entry

from lists import building_list
from lists import continent_list
from lists import deity_list
from lists import equipment_list
from lists import monster_list
from lists import evolution_list
from lists import servant_list
from lists import spell_list
from lists import tech_list
# from lists import tech_list_new as tech_list
from lists import trait_list
from lore import page_saver

from functions import path_preprocessor_f

# from data import path_preprocessor

# A link from a main table to either another main or a list
def main(fix = False, show_fixes=False):
	output = []
	
	# This allows for easy swapping
	pr = output.append
	pr = print
	
	cursor = database.get_cursor()
	
	if fix:	pr(database.shell_text("\n''Checking and fixing tables''"))
	else:	pr(database.shell_text("\n''Checking tables''"))
	
	#	Classes
	#------------------------
	
	# Stuff that relies on other stuff
	pr(sync_f.check_table(cursor, campaign.Campaign().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, battle.Battle().table_info, fix, show_fixes))
	
	# Artefacts
	pr(sync_f.check_table(cursor, artefact.Artefact().table_info, fix, show_fixes))
	
	# Armies
	pr(sync_f.check_table(cursor, army.Army().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, army.Army_monsters, fix, show_fixes))
	# pr(sync_f.check_table(cursor, army.Army_battle_history, fix, show_fixes))
	
	# Battle
	# pr(sync_f.check_table(cursor, battle.Battle_teams, fix, show_fixes))
	# pr(sync_f.check_table(cursor, battle.Proposed_losses, fix, show_fixes))
	
	# Campaign
	pr(sync_f.check_table(cursor, campaign.Campaign_teams, fix, show_fixes))
	pr(sync_f.check_table(cursor, campaign.Campaign_armies, fix, show_fixes))
	
	# Cities
	pr(sync_f.check_table(cursor, city.City().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, city.City_buildings, fix, show_fixes))
	pr(sync_f.check_table(cursor, city.Trade_distances, fix, show_fixes))
	
	# Logs
	pr(sync_f.check_table(cursor, log.Log().table_info, fix, show_fixes))
	
	# Map stuff
	pr(sync_f.check_table(cursor, mapper.Map_terrain().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, mapper.Map_continent().table_info, fix, show_fixes))
	
	# Missions
	pr(sync_f.check_table(cursor, mission.Mission().table_info, fix, show_fixes))
	
	# Operatives
	pr(sync_f.check_table(cursor, operative.Operative().table_info, fix, show_fixes))
	
	# Orders
	pr(sync_f.check_table(cursor, order_post.Order_post({}).table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, intorder.Intorder({}).table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, order_post.interactive_orders, fix, show_fixes))
	
	# Players
	pr(sync_f.check_table(cursor, player.Player().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, player.Player_history, fix, show_fixes))
	pr(sync_f.check_table(cursor, player.Player_kills, fix, show_fixes))
	
	# Powers
	pr(sync_f.check_table(cursor, power.Power().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, power.Power_history, fix, show_fixes))
	
	# Queries
	pr(sync_f.check_table(cursor, queries.Query().table_info, fix, show_fixes))
	
	# Results
	pr(sync_f.check_table(cursor, results.Result().table_info, fix, show_fixes))
	
	# Spy report
	pr(sync_f.check_table(cursor, spy_report.Spy_report().table_info, fix, show_fixes))
	
	# Squad
	pr(sync_f.check_table(cursor, squad.Squad().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, squad.Squad_battle_history, fix, show_fixes))
	
	# Stat
	pr(sync_f.check_table(cursor, stat.Stat().table_info, fix, show_fixes))
	
	# Team
	pr(sync_f.check_table(cursor, team.Team().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_resources, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_relations, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Border_history, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_deities, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_evolutions, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_spells, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_techs, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_json_ti, fix, show_fixes))
	pr(sync_f.check_table(cursor, team.Team_traits, fix, show_fixes))
	
	# Turn
	pr(sync_f.check_table(cursor, turn.Turn().table_info, fix, show_fixes))
	
	# Unit
	pr(sync_f.check_table(cursor, unit.Unit().table_info, fix, show_fixes))
	pr(sync_f.check_table(cursor, unit.Unit_equipment, fix, show_fixes))
	
	# Wonder
	pr(sync_f.check_table(cursor, wonder.Wonder().table_info, fix, show_fixes))
	
	#	Lists
	#------------------------
	pr(sync_f.fill_table(cursor, building.Building().table_info, building_list))
	pr(sync_f.fill_table(cursor, deity.Deity().table_info, deity_list))
	pr(sync_f.fill_table(cursor, equipment.Equipment().table_info, equipment_list))
	pr(sync_f.fill_table(cursor, evolution.Evolution().table_info, evolution_list))
	pr(sync_f.fill_table(cursor, monster.Monster().table_info, monster_list))
	pr(sync_f.fill_table(cursor, servant.Servant().table_info, servant_list))
	pr(sync_f.fill_table(cursor, spell.Spell().table_info, spell_list))
	pr(sync_f.fill_table(cursor, tech.Tech().table_info, tech_list))
	pr(sync_f.fill_table(cursor, trait.Trait().table_info, trait_list))
	
	# Rebuilds the tables internally due to a non-linear data structure
	page_saver.rebuild_pages(cursor)
	
	if fix:
		build_map(cursor)
	
	# database.conn.commit()
	if fix:
		pr("\nCommited changes\n")
	
	if pr == output.append:
		try:
			return "\n".join(output)
		except Exception as e:
			print(output)
			raise
	else:
		return ""

def build_map(cursor=None):
	if cursor == None:
		cursor = database.get_cursor()
	
	# Drop the map_continent_tiles table
	query = "DROP TABLE map_continent_tiles"
	try: cursor.execute(query)
	except Exception as e:
		pass
	
	# Map preprocessor
	sync_f.fill_table(cursor, mapper.Map_continent().table_info, continent_list)
	sync_f.check_table(cursor, mapper.Map_continent_tiles, fix=True, show_fixes=False)
	
	path_preprocessor_f.run(cursor)
