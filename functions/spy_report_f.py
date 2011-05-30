import random
import re
import math
import collections
from classes import spy_report, unit

empty_report = spy_report.empty_report

def _success(success_chance):
	if success_chance >= 1:
		return True
	
	if random.random() < success_chance:
		return True
	
	return False

def distort(value, success_chance):
	if success_chance >= 1:
		return value
		
	roll = random.random()
	
	if roll <= success_chance:
		return value
	
	# High success chance means a lower difference
	diff = max(roll - success_chance, 0)
	
	if random.random() > 0.5:
		return value * (1 + diff)
	else:
		return value * (1 - diff)

# steps = (1, 10, 100, 500, 1000, 5000, 10000, 50000, 100000)
steps = []
i = 10
while i < 10000000:
	i += round(i/3)
	if i > 10000:
		steps.append(round(i, -4))
	elif i > 1000:
		steps.append(round(i, -3))
	elif i > 100:
		steps.append(round(i, -2))
	else:
		steps.append(round(i, -1))

def approx(n):
	for s in steps:
		if n > s: continue
		return "Less than {0}".format(s)

# Actual reports
def _city_buildings(the_world, area, radius, success=1):
	result = empty_report({"report_type":"City buildings"})
	completed, in_progress = [], []
	content = []
	
	city_dict = the_world.cities()
	building_dict = the_world.buildings()
	cities_in_area = the_world.cities_in_area(area, radius)
	
	for c in cities_in_area:
		the_city = city_dict[c]
		
		# Buildings complete
		for b, amount in the_city.buildings_amount.items():
			if amount != 0:
				if _success(success):
					if amount > 1:
						completed.append("%s x%d" % (building_dict[b].name, amount))
					else:
						completed.append(building_dict[b].name)
		
		# Buildings in progress
		for b, progress in the_city.buildings.items():
			if progress != 0:
				if _success(success):
					in_progress.append("%s" % (building_dict[b].name))
		
		# Format to string
		content.append("[b]{name}[/b]".format(
			name=the_city.name
		))
		if completed != []:
			content.append("Completed: {0}".format(", ".join(completed)))
		if in_progress != []:
			content.append("In progress: {0}".format(", ".join(in_progress)))
		
		if completed == [] and in_progress == []:
			content.append("No buildings")
		
		content.append("")
	
	result.content = "\n".join(content)
	return result

def _armies_basic(the_world, area, radius, success=1):
	result = empty_report({"report_type":"Armies basic"})
	completed, in_progress = [], []
	content = []
	
	army_dict = the_world.armies()
	team_dict = the_world.teams()
	armies_in_area = the_world.armies_in_area(area, radius)
	
	for a in armies_in_area:
		the_army = army_dict[a]
		
		if not team_dict[the_army.team].active:
			continue
		
		# Format to string
		content.append("[b]{name}[/b] {team}".format(
			name=the_army.name,
			team=team_dict[the_army.team].name
		))
		
		content.append("Size: {0}".format(
			approx(distort(the_army.get_size(the_world.cursor), success))
		))
		
		content.append("")
	
	result.content = "\n".join(content)
	return result

def _armies_units(the_world, area, radius, success=1):
	result = empty_report({"report_type":"Armies units"})
	completed, in_progress = [], []
	content = []
	
	team_dict = the_world.teams()
	army_dict = the_world.armies()
	unit_dict = the_world.units()
	armies_in_area = the_world.armies_in_area(area, radius)
	
	cities_in_area = the_world.cities_in_area(area, radius)
	for c in cities_in_area:
		armies_in_area.extend(the_world.armies_by_base(c))
	
	armies_in_area = list(set(armies_in_area))
	
	for a in armies_in_area:
		the_army = army_dict[a]
		
		if not team_dict[the_army.team].active:
			continue
		
		# Format to string
		content.append("[b]{name}[/b] - {team}".format(
			name=the_army.name,
			team=team_dict[the_army.team].name
		))
		
		unit_count = {}
		for s, the_squad in the_army.squads.items():
			if the_squad.unit not in unit_count:
				unit_count[the_squad.unit] = 0
			
			unit_count[the_squad.unit] += distort(the_squad.amount, success)
		
		for u, amount in unit_count.items():
			if amount < 1: continue
			content.append("{amount} {name} ({weapon_cat}, {armour_cat}, {move_cat}, {training_cat} training)".format(
				amount = approx(amount),
				name = unit_dict[u].name,
				weapon_cat = unit.weapon_categories[unit_dict[u].weapon_cat],
				armour_cat = unit.armour_categories[unit_dict[u].armour_cat],
				move_cat = unit.move_categories[unit_dict[u].move_cat],
				training_cat = unit.training_categories[unit_dict[u].training_cat],
			))
		
		content.append("")
	
	result.content = "\n".join(content)
	return result

def _armies_depth(the_world, area, radius, success=1):
	result = empty_report({"report_type":"Armies depth"})
	completed, in_progress = [], []
	content = []
	
	team_dict = the_world.teams()
	army_dict = the_world.armies()
	unit_dict = the_world.units()
	armies_in_area = the_world.armies_in_area(area, radius)
	
	for a in armies_in_area:
		the_army = army_dict[a]
		
		if not team_dict[the_army.team].active:
			continue
		
		# Format to string
		content.append("[b]{name}[/b] {team}".format(
			name=the_army.name,
			team=team_dict[the_army.team].name
		))
		
		unit_count = {}
		for s, the_squad in the_army.squads.items():
			if the_squad.unit not in unit_count:
				unit_count[the_squad.unit] = 0
			
			unit_count[the_squad.unit] += distort(the_squad.amount, success)
		
		for u, amount in unit_count.items():
			if amount < 1: continue
			content.append("{0} {1} - {2}".format(
				approx(amount),
				unit_dict[u].name,
				unit_dict[u].equipment_string,
			))
		
		content.append("")
	
	result.content = "\n".join(content)
	return result


mission_types = collections.OrderedDict()

mission_types["City buildings"] = spy_report.Mission("City buildings", _city_buildings, "Certain")
mission_types["Armies basic"] = spy_report.Mission("Armies basic", _armies_basic, "Basic observation")
mission_types["Armies units"] = spy_report.Mission("Armies units", _armies_units, "Basic observation")
mission_types["Armies depth"] = spy_report.Mission("Armies depth", _armies_depth, "Basic observation")

def run_mission(the_world, team_id, area, radius, mission_name):
	the_mission = mission_types[mission_name]
	success = 1
	
	return the_mission.run(the_world, team_id, area, radius)

# Wrapper function for making reports
def generate_report(the_world, team_id, city_id, area, radius, report_types=[]):
	city_dict = the_world.cities()
	
	# Get area
	if area == "":
		the_city = city_dict[city_id]
		x, y = the_city.x, the_city.y
	
	else:
		res = re.search(r"(-?[0-9]*)[,:] ?(-?[0-9]*)", area)
		x = int(res.groups()[0])
		y = int(res.groups()[1])
	
	# Possibly use all report types
	if report_types == []:
		for k, v in mission_types.items():
			report_types.append(k)
	
	output = []
	for r in report_types:
		# output.append(run_mission(the_world, team_id, (x, y), radius, r))
		output.append(mission_types[r](the_world, team_id, (x, y), radius))
	
	return output
	

