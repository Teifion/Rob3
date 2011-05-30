from pages import common
from queries import team_q, campaign_q
from functions import stat_f
from rules import team_rules
from classes import world
import collections

page_data = {
	"Title":	"Evo points",
	"Admin":	True,
}

def main(cursor):
	team_dict = team_q.get_real_active_teams(cursor)
	
	# Caching
	team_q.mass_get_team_resources(cursor, team_dict)
	
	# Defaults
	largest_army_id			= -1
	largest_army_size		= -1
	
	largest_navy_id			= -1
	largest_navy_size		= -1
	
	most_materials_id		= -1
	most_materials_size		= -1
	
	most_population_id		= -1
	most_population_size	= -1
	
	most_slaves_id			= -1
	most_slaves_size		= -1
	
	most_mages_id			= -1
	most_mages_size			= -1
	
	most_operatives_id		= -1
	most_operatives_size	= -1
	
	most_land_id			= -1
	most_land_size			= -1
	
	for t, the_team in team_dict.items():
		#	LARGEST ARMY?
		#------------------------
		size = team_q.get_army_size(cursor, the_team.id)
		if size > largest_army_size:
			largest_army_size	= size
			largest_army_id		= t
	
		#	LARGEST NAVY?
		#------------------------
		size = team_q.get_navy_size(cursor, the_team.id)
		if size > largest_navy_size:
			largest_navy_size	= size
			largest_navy_id		= t
		
		#	RICHEST NATION
		#------------------------
		if the_team.resources.get("Materials") > most_materials_size:
			most_materials_size	= the_team.resources.get("Materials")
			most_materials_id	= t
		
		#	LARGEST POPULATION
		#------------------------
		if the_team.get_population(cursor) > most_population_size:
			most_population_size	= the_team.get_population(cursor)
			most_population_id		= t
		
		#	MOST SLAVES
		#------------------------
		if the_team.get_slaves(cursor) > most_slaves_size:
			most_slaves_size	= the_team.get_slaves(cursor)
			most_slaves_id		= t
		
		#	MOST MAGES
		#------------------------
		size = team_q.get_mage_count(cursor, the_team.id)
		if size > most_mages_size:
			most_mages_size	= size
			most_mages_id	= t
		
		#	MOST OPERATIVES
		#------------------------
		if the_team.operative_count(cursor) > most_operatives_size:
			most_operatives_size	= the_team.operative_count(cursor)
		most_operatives_id	= t
	
		#	LAND CONTROLLED
		#------------------------
		stat_f.check_team_stats(cursor, the_team)
		team_stats = the_team.get_stats(cursor)
		
		if team_stats[common.current_turn()].land_controlled > most_land_size:
			most_land_size	= team_stats[common.current_turn()].land_controlled
			most_land_id	= t
	
	# Formatting
	largest_army_size = common.number_format(largest_army_size)
	largest_navy_size = common.number_format(largest_navy_size)
	
	most_materials_size = common.number_format(int(most_materials_size))
	
	most_population_size = common.number_format(most_population_size)
	most_slaves_size = common.number_format(most_slaves_size)
	
	most_mages_size = common.number_format(most_mages_size)
	most_operatives_size = common.number_format(most_operatives_size)
	
	most_land_size = round(most_land_size, 2)
	
	output = []
	the_world = world.World(cursor)
	for t, the_team in team_dict.items():
		output.append("\n\t%s" % the_team.name)
	
		# Military
		if largest_army_id == t: output.append("1: Largest army (%s)" % largest_army_size)
		if largest_navy_id == t: output.append("1: Largest navy (%s)" % largest_navy_size)
	
		# Resources
		if most_materials_id == t: output.append("1: Richest nation (%s)" % most_materials_size)
	
		produced_resources, new_resources = team_rules.produce_resources(cursor, the_team, the_world)
		
		if new_resources.get("Iron") > 0 and new_resources.get("Stone") > 0 and new_resources.get("Wood") > 0:
			output.append("2: Own a supply of each resource")
	
		# Population
		if most_population_id == t: output.append("1: Most population (%s)" % most_population_size)
		if most_slaves_id == t: output.append("1: Most slaves (%s)" % most_slaves_size)
	
		# Special units
		if most_mages_id == t: output.append("1: Most mages (%s)" % most_mages_size)
		if most_operatives_id == t: output.append("1: Most operatives (%s)" % most_operatives_size)
	
		# Land controlled
		if most_land_id == t: output.append("1: Most land controlled (%s)" % most_land_size)
	
		#	campaigns
		#------------------------
		campaign_dict = campaign_q.get_campaigns_from_team(cursor, t, include_secret=True, since_turn=common.current_turn()-4)
		
		team_war_count = 0
		team_campaign_dict = {}
		
		# if t == 71:
		# 	print("")
		# 	for k, v in campaign_dict.items():
		# 		print(v.name, " - ", v.turn, "<br />")
		
		if campaign_dict != ([], {}):
			for k, the_campaign in campaign_dict.items():
				team_campaign_dict[the_campaign.turn] = True
			
			if len(team_campaign_dict) == 1:
				output.append("1: Only one year with a war")
			
			elif len(team_campaign_dict) > 1:
				output.append("%s: %s years with wars" % (len(team_campaign_dict), len(team_campaign_dict)))
		
		
		
		# Roleplay?
		output.append("? 1: Good roleplay")
	
	return '&nbsp;<textarea rows="40" style="width:99%%;">%s</textarea>' % "\n".join(output)