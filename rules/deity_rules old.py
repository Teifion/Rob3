from pages import common
from classes import res_dict
from queries import team_q
from functions import campaign_f, path_f, stat_f, team_f
from rules import team_rules

favour_rewards = {
# Pos = good
# Neg = bad
	"major_pos":	3,
	"major_neg":	0,
	
	"minor_pos":	1,
	"minor_neg":	0,
	
	"negative_pos":	0,
	"negative_neg":	-2,
}

def Arl(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: End the turn with at least 1 more city than you started it with
	#------------------------
	def major():
		team_stats		= the_team.get_stats(the_world.cursor)
		
		try:
			cities_this_turn = team_stats[common.current_turn()].city_count
		except Exception:
			cities_this_turn = 0
		
		if (common.current_turn()-1) not in team_stats:
			cities_last_turn = 0
		else:
			cities_last_turn = team_stats[common.current_turn()-1].city_count
		
		if cities_this_turn > cities_last_turn:
			info.append("<span class='pos'>Major:</span> You have at least 1 more city this turn than the last")
			return favour_rewards["major_pos"]
		else:
			info.append("<span class='neg'>Major:</span> You do not have at least 1 more city this turn than the last")
			return favour_rewards["major_neg"]
	
	#	Minor: All of your cities are within 100 units of another nation's city
	#------------------------
	def minor():
		city_dict = the_world.cities()
		
		failures = []
		for k, our_city in city_dict.items():
			city_is_within_range = False
			
			if our_city.team != the_team.id: continue# We only want to use our own cities thanks
			if our_city.dead: continue
			
			for k, their_city in city_dict.items():
				if city_is_within_range: continue# We've approved this one already
				
				if their_city.team == the_team.id: continue# Ignore ourselves
				if their_city.dead: continue# Ignore dead cities
				
				distance = path_f.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance < 100: city_is_within_range = True
			
			if not city_is_within_range:
				failures.append(our_city.name)
		
		if len(failures) == 0:
			info.append("<span class='pos'>Minor:</span> All of your cities are within 100 units of a city from another nation")
			return favour_rewards["minor_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Minor:</span> The following cities are not within 100 units of a city from another nation: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Minor:</span> The city %s is not within 100 units of a city from another nation" % (failures[0]))
			return favour_rewards["minor_neg"]
			
	
	#	Negative: At least as many civilians as last turn
	#------------------------
	def negative():
		team_stats		= the_team.get_stats(the_world.cursor)
		
		try:
			pop_this_turn = team_stats[common.current_turn()].population
		except Exception:
			pop_this_turn = 250
		
		if (common.current_turn()-1) not in team_stats:
			pop_last_turn = 250
		else:
			pop_last_turn = team_stats[common.current_turn()-1].population
		
		if pop_this_turn > pop_last_turn:
			info.append("<span class='pos'>Negative:</span> You have at least as many civilians as last turn")
			return favour_rewards["negative_pos"]
		else:
			info.append("<span class='neg'>Negative:</span> You have fewer civilians than you did last turn")
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Trchkithin(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: Trchkithin nations control at least 40% of the chosen land
	#------------------------
	def major():
		team_dict		= the_world.teams()
		deities_lookup	= the_world.deities_lookup()
		
		total_control = 0
		trch_control = 0
		for team_id, t in team_dict.items():
			if t.ir: continue
			if not t.active: continue
			
			stat_f.check_team_stats(the_world.cursor, t, the_world)
			team_stats = t.get_stats(the_world.cursor)
			
			if common.current_turn() in team_stats:
				if deities_lookup['Trchkithin'] in t.get_deities(the_world.cursor):
					trch_control += team_stats[common.current_turn()].land_controlled
				
				total_control += team_stats[common.current_turn()].land_controlled
		
		if total_control == 0:
			trch_control_percent = 0
		else:
			trch_control_percent = round(100*trch_control/float(total_control), 2)
		if trch_control_percent >= 40:
			info.append("<span class='pos'>Major:</span> Trchkithin nations control over 40%% of the land controlled by Chosen ones (%s%%)" % (trch_control_percent))
			
			if the_team.name == "Holy Empire of Machtburg":
				return favour_rewards["major_pos"] + 1
			
			return favour_rewards["major_pos"]
		else:
			info.append("<span class='neg'>Major:</span> Trchkithin nations control under 40%% of the land controlled by Chosen ones (%s%%)" % (trch_control_percent))
			
			if the_team.name == "Holy Empire of Machtburg":
				return favour_rewards["major_neg"] + 1
			
			return favour_rewards["major_neg"]
	
	#	Minor: Your slave count is at least 20% the size of your population
	#------------------------
	def minor():
		slave_size	= the_team.get_slaves(the_world.cursor)
		pop_size	= the_team.get_population(the_world.cursor)
		
		# Prevent divide by 0 rubbish
		pop_size = max(pop_size, 1)
		
		slave_percent = int((float(slave_size)/float(pop_size))*100)
		if slave_percent:
			info.append("<span class='pos'>Minor:</span> You have at least 1 slave for every 5 people (%s%%)" % (slave_percent))
			return favour_rewards["minor_pos"]
		else:
			if slave_size == 0:
				info.append("<span class='neg'>Minor:</span> You have no slaves, you need at least 1 for every 5 people (%s)" % (pop_size/5.0))
			elif slave_size == 1:
				info.append("<span class='neg'>Minor:</span> You have only one slave, you need at least 1 for every 5 people (%s)" % (pop_size/5.0))
			else:
				info.append("<span class='neg'>Minor:</span> You have only %s slaves (need at least %s)" % (slave_size, pop_size/5.0))
			return favour_rewards["minor_neg"]
	
	#	Negative: A city within 200 map units follows Arl
	#------------------------
	def negative():
		city_dict		= the_world.cities()
		team_dict		= the_world.teams()
		deities_lookup	= the_world.deities_lookup()
		
		failures = []
		for k, our_city in city_dict.items():
			city_failure = ""
			
			if our_city.team != the_team.id: continue# We only want to use our own cities thanks
			if our_city.dead: continue
			
			for k, their_city in city_dict.items():
				if city_failure != "": continue# We've failed this one already
				if deities_lookup['Arl'] not in team_dict[their_city.team].get_deities(the_world.cursor): continue
				
				if their_city.team == the_team.id: continue# Ignore ourselves
				if their_city.dead: continue# Ignore dead cities
				
				distance = path_f.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance < 200:
					city_failure = their_city.name
					failures.append("%s (%s)" % (our_city.name, city_failure))
		
		if len(failures) < 1:
			info.append("<span class='pos'>Negative:</span> No Arl aligned cities are within 200 units of any of your cities")
			return favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Negative:</span> The following cities are within 200 units of an Arl aligned city: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Negative:</span> The city of %s is within 200 units of an Arl aligned city" % (failures[0]))
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Adyl(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: All cities of 30k or more must are walled
	#------------------------
	def major():
		city_dict		= the_world.cities()
		our_cities		= the_world.cities_from_team(the_team.id)
		
		failures = []
		for k, our_city in our_cities.items():
			if our_city.dead: continue
			
			if our_city.population + our_city.slaves >= 20000:
				if not our_city.walled:
					failures.append(our_city.name)
		
		if len(failures) == 0:
			info.append("<span class='pos'>Major:</span> All of your cities larger than 20k people are walled")
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following cities are larger than 20,000 people and not walled: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> Your city of %s is larger than 20,000 people is not walled")
			return favour_rewards["major_neg"]
	
	#	Minor: Participated in a war
	#------------------------
	def minor():
		if campaign_f.team_campaign_count(the_world.cursor, the_team.id, common.current_turn()) > 0:
			info.append("<span class='pos'>Minor:</span> You participated in at least one war")
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> You did not participate in any wars")
			return favour_rewards["minor_neg"]
	
	#	Negative: Posses any troops with training below normal
	#------------------------
	def negative():
		our_cities		= the_world.cities_from_team(the_team.id)
		team_dict		= the_world.teams()
		
		failures = []
		for k, our_city in our_cities.items():
			if our_city.dead: continue
			
			if our_city.population + our_city.slaves >= 30000:
				if not our_city.walled:
					failures.append(our_city.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Negative:</span> All cities larger than 30,000 have a wall")
			return favour_rewards["negative_pos"]
		else:
			if len(failures) == 1:
				info.append("<span class='neg'>Negative:</span> The city of %s has no wall" % (failures[0]))
			else:
				info.append("<span class='neg'>Negative:</span> The following cities have no wall: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			
			return favour_rewards["negative_pos"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Ssai(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: Must have an operative within every nation that has a city within 1000 units of one of yours
	#------------------------
	def major():
		team_dict_c			= the_world.teams()
		city_dict_c			= the_world.cities()
		operatives_dict_c	= the_world.operatives()
		
		the_world.operatives_in_city(0)
		operatives_by_city	= the_world._operatives_in_city
		
		# First we want a list of all our cities
		our_city_list = []
		their_city_list = []
		
		for city_id, the_city in city_dict_c.items():
			if the_city.dead > 0: continue
			
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			elif common.current_turn() - the_city.founded > 2:
				their_city_list.append(city_id)
		
		nations_within_range	= set()
		nations_infiltrated		= set()
		
		# New we compare each with each
		for our_city_id in our_city_list:
			our_city = city_dict_c[our_city_id]
			
			for their_city_id in their_city_list:
				their_city = city_dict_c[their_city_id]
				
				# Is this city within range?
				distance = path_f.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance <= 1000:
					nations_within_range.add(their_city.team)
					
					if their_city_id in operatives_by_city:
						city_has_op = False
						for o in operatives_by_city[their_city_id]:
							if operatives_dict_c[o].team == the_team.id and operatives_dict_c[o].died < 1:
								city_has_op = True
						
						if city_has_op:
							nations_infiltrated.add(their_city.team)
		
		# Now to find out what nations we fail at
		failures = []
		for t in nations_within_range:
			if t not in nations_infiltrated:
				failures.append(team_dict_c[t].name)
		
		if len(failures) == 0:
			info.append("<span class='pos'>Major:</span> You have operatives within all nations within 1000 units of your cities" % (operative_percentage))
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following nations do not have operatives in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> The nation of %s does not have an operative in it" % (failures[0]))
			return favour_rewards["major_neg"]
	
	#	Minor: At least 1 operative per 1000 troops
	#------------------------
	def minor():
		army_size	= team_q.get_army_size(the_world.cursor, the_team.id) + team_q.get_navy_size(the_world.cursor, the_team.id) + team_q.get_airforce_size(the_world.cursor, the_team.id)
		op_count	= the_team.operative_count(the_world.cursor)
		
		if army_size == 0:	op_ratio = 1
		else:				op_ratio = round(op_count*1000/army_size, 2)
		
		if op_ratio >= 1:
			info.append("<span class='pos'>Minor:</span> You have more than 1 spy per 1000 troops (%s per 1000)" % (op_ratio))
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> You have fewer than 1 spy per 1000 troops (%s per 1000)" % (op_ratio))
			return favour_rewards["minor_neg"]
			
	
	#	Negative: A city within 100 units of one of yours is over 2 years old and is not infiltrated
	#------------------------
	def negative():
		team_dict_c			= the_world.teams()
		city_dict_c			= the_world.cities()
		operatives_dict_c	= the_world.operatives()
		
		the_world.operatives_in_city(0)
		operatives_by_city	= the_world._operatives_in_city
		
		# First we want a list of all our cities
		our_city_list = []
		their_city_list = []
		
		failures = []
		for city_id, the_city in city_dict_c.items():
			if the_city.dead > 0: continue
			
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			elif common.current_turn() - the_city.founded > 2:
				their_city_list.append(city_id)
		
		# New we compare each with each
		for our_city_id in our_city_list:
			our_city = city_dict_c[our_city_id]
			
			for their_city_id in their_city_list:
				their_city = city_dict_c[their_city_id]
				
				# Is this city within range?
				distance = path_f.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance <= 100:
					# Check for operative
					if their_city_id in operatives_by_city:
						city_has_op = False
						for o in operatives_by_city[their_city_id]:
							if operatives_dict_c[o].team == the_team.id and operatives_dict_c[o].died < 1:
								city_has_op = True
						
						if not city_has_op:
							failures.append(their_city.name)
					else:
						failures.append(their_city.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Negative:</span> All cities older than 2 years and within 100 units of one of your cities have an operative in them")
			return favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Negative:</span> The following foreign cities do not have operatives in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Negative:</span> The foreign city of %s does not have an operative in it" % (failures[0]))
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Orakt(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: Upkeep is at least 25% of your income
	#------------------------
	def major():
		upkeep = team_f.get_upkeep(the_team, the_world)
		income = team_rules.produce_resources(the_world.cursor, the_team, the_world)[0].get("Materials")
		
		if income == 0:
			percentage = 100
		else:
			percentage = round(upkeep/float(income)*100, 2)
		
		if income <= (upkeep * 4):
			info.append("<span class='pos'>Major:</span> Your military upkeep is at least 25%% of your income (%s%%)" % percentage)
			return favour_rewards["major_pos"]
		else:
			info.append("<span class='neg'>Major:</span> Your military upkeep is less that 25%% of your income (%s%%)" % percentage)
			return favour_rewards["major_neg"]
		
	
	#	Minor: Participated in at least 3 wars this turn
	#------------------------
	def minor():
		if campaign_f.team_campaign_count(the_world.cursor, the_team.id, common.current_turn()) >= 1:
			info.append("<span class='pos'>Minor:</span> You participated in at least three wars")
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> You participated in fewer than 3 wars this year")
			return favour_rewards["minor_neg"]
	
	#	Negative: Participated in 0 wars
	#------------------------
	def negative():
		if campaign_f.team_campaign_count(the_world.cursor, the_team.id, common.current_turn()) > 0:
			info.append("<span class='pos'>Negative:</span> You participated in one or more wars")
			return favour_rewards["negative_pos"]
		else:
			info.append("<span class='neg'>Negative:</span> You participated in no wars")
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Agashn(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: Above average land control
	#------------------------
	def major():
		team_dict		= the_world.teams()
		
		total_control = 0
		team_count = 0
		our_control = 0
		for team_id, t in team_dict.items():
			# if t.id == the_team.id: continue
			if t.ir: continue
			if not t.active: continue
			
			stat_f.check_team_stats(the_world.cursor, t, the_world)
			team_stats = t.get_stats(the_world.cursor)
			
			if common.current_turn() in team_stats:
				total_control += team_stats[common.current_turn()].land_controlled
			
			team_count += 1
			
			if t.id == the_team.id:
				if common.current_turn() in team_stats:
					our_control = team_stats[common.current_turn()].land_controlled
				else:
					our_control = 0
		
		average_control = total_control/float(team_count)
		
		if average_control <= our_control:
			info.append("<span class='pos'>Major:</span> You have above average land control of %s, average is %s" % (our_control, average_control))
			return favour_rewards["major_pos"]
		else:
			info.append("<span class='neg'>Major:</span> You have below average land control of %s, average is %s" % (our_control, average_control))
			return favour_rewards["major_neg"]
			
	
	#	Minor: Army is at least 15% the size of your population
	#------------------------
	def minor():
		army_size	= team_q.get_unit_category_size(the_world.cursor, the_team.id, 0, 100)
		pop_size	= the_team.get_population(the_world.cursor)
		
		if pop_size == 0:
			army_percent = 100
		else:
			army_percent = int((float(army_size)/float(pop_size))*100)
		if army_percent >= 15:
			info.append("<span class='pos'>Minor:</span> Your armed forces are at least 15%% the size of your population (%s%%)" % (army_percent))
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> Your armed forces are less than 15%% the size of your population (currently %s, need at least %s)" % (army_size, pop_size/5))
			return favour_rewards["minor_neg"]
	
	#	Negative: End the turn with fewer cities than you started with
	#------------------------
	def negative():
		team_stats		= the_team.get_stats(the_world.cursor)
		
		if (common.current_turn()-1) not in team_stats:
			cities_this_turn = 1
			cities_last_turn = 0
		else:
			cities_this_turn = team_stats[common.current_turn()].city_count
			cities_last_turn = team_stats[common.current_turn()-1].city_count
		
		if cities_this_turn >= cities_last_turn:
			info.append("<span class='pos'>Negative:</span> You have ended this year with at least as many cities as you ended last year with")
			return favour_rewards["negative_pos"]
		else:
			info.append("<span class='neg'>Negative:</span> You have ended this year with 1 or more fewer cities than last year")
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Ldura(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: All cities larger than 50k have an expanded university and expanded academy
	#------------------------
	def major():
		city_dict		= the_world.cities()
		team_dict		= the_world.teams()
		building_lookup	= the_world.buildings_lookup()
		
		failures = []
		for city_id, the_city in city_dict.items():
			if the_city.team != the_team.id: continue# We only want to use our own cities thanks
			if the_city.dead > 0: continue
			if the_city.nomadic: continue
			
			if the_city.population + the_city.slaves >= 50000:
				city_buildings, city_buildings_amount = the_city.get_buildings(the_world.cursor)
				
				if building_lookup["Expanded academy"] not in city_buildings_amount or \
					building_lookup["Expanded university"] not in city_buildings_amount:
					failures.append(the_city.name)
		
		if len(failures) == 0:
			info.append("<span class='pos'>Major:</span> All of your cities larger than 50,000 people possess both an expanded academy and university")
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following cities are larger than 50,000 people and not in possession of an expanded academy and university: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> Your city of %s is larger than 50,000 people is not in possession of an expanded acadamy and university")
			return favour_rewards["major_neg"]
		
	
	#	Minor: Every city has a university and an academy before anything else except walls
	#------------------------
	def minor():
		city_dict		= the_world.cities()
		team_dict		= the_world.teams()
		building_lookup	= the_world.buildings_lookup()
		building_dict	= the_world.buildings()
		
		academy_type_list = [building_lookup["Academy"], building_lookup["Expanded academy"], building_lookup["Academy of Light"], building_lookup["Academy of Dark"], building_lookup["Academy of Abjuration"], building_lookup["Academy of Destruction"], building_lookup["Academy of Daemonic"], building_lookup["Academy of Necromancy"]]
		university_type_list = [building_lookup["University"], building_lookup["Expanded university"]]
		
		failures = []
		for city_id, the_city in city_dict.items():
			if the_city.team != the_team.id: continue# We only want to use our own cities thanks
			if the_city.dead > 0: continue
			if the_city.nomadic: continue
			
			city_buildings, city_buildings_amount = the_city.get_buildings(the_world.cursor)
			
			city_has_academy = False
			city_has_university = False
			city_has_others = False
			
			for b in city_buildings_amount:
				# The dict may have values of 0 in it, we need to skip these
				if city_buildings_amount[b] < 1: continue
				if building_dict[b].wall: continue
				
				# Buildings we want to have
				if b in academy_type_list:		city_has_academy = True
				elif b in university_type_list:	city_has_university = True
				else:							city_has_others = True
			
			if city_has_others:
				if not city_has_academy or not city_has_university:
					failures.append(the_city.name)
		
		if len(failures) == 0:
			info.append("<span class='pos'>Minor:</span> All of your cities have an academy and a university or no other buildings")
			return favour_rewards["minor_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following cities do not have an academy and university but do have other buildings: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> Your city of %s has no academy and university but does have other buildings" % failures[0])
			return favour_rewards["minor_neg"]
	
	#	Negative: Participated in more than 1 war
	#------------------------
	def negative():
		if campaign_f.team_campaign_count(the_world.cursor, the_team.id, common.current_turn()) > 1:
			info.append("<span class='neg'>Negative:</span> You participated in more than one war this year")
			return favour_rewards["negative_neg"]
		else:
			info.append("<span class='pos'>Negative:</span> You participated in one or fewer wars this year")
			return favour_rewards["negative_pos"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Azmodius(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: You have no mages
	#------------------------
	def major():
		unit_dict_c			= data.unit.get_unit_dict_c()
		equipment_dict_n	= data.equipment.get_equipment_dict_n()
		squad_dict_c		= squad.get_squad_dict_c()
		
		failures = []
		magic_units = [1,2,3,4,5,6,7,8,9]# Default mages
		for unit_id, our_unit in unit_dict_c.items():
			if our_unit.team != the_team.id: continue
			
			unit_equipment = our_unit.get_equipment()
			if equipment_dict_n["Low tier magic"] in unit_equipment or \
				equipment_dict_n["Mid tier magic"] in unit_equipment or \
				equipment_dict_n["High tier magic"] in unit_equipment:
				magic_units.append(unit_id)
		
		for squad_id, the_squad in squad_dict_c.items():
			if the_squad.team != the_team.id: continue
			if the_squad.amount < 1: continue
			
			if the_squad.unit in magic_units:
				failures.append(the_squad.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Major:</span> You have no mages")
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Negative:</span> You have mages in the following squads: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Negative:</span> The squad of %s has mages in it" % (failures[0]))
			
			return favour_rewards["negative_pos"]
	
	#	Minor: Your army is at least 20% the size of your population (yes it's the same as Agashn)
	#------------------------
	def minor():
		army_size	= the_team.army_size() + the_team.navy_size() + the_team.airforce_size()
		pop_size	= the_team.get_population()
		
		army_percent = int((float(army_size)/float(pop_size))*100)
		if army_percent >= 20:
			info.append("<span class='pos'>Minor:</span> Your armed forces are at least 20%% the size of your population (%s%%)" % (army_percent))
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> Your armed forces are less than 20%% the size of your population (currently %s, need at least %s)" % (army_size, pop_size/5))
			return favour_rewards["minor_neg"]
	
	#	Negative: A city within 150 units of one of yours has an expanded or specialised academy
	#------------------------
	def negative():
		team_dict_c		= data.team.get_teams_dict_c()
		city_dict_c		= city.get_city_dict_c()
		building_dict_n	= building.get_building_dict_n()
		
		academy_type_list = [building_dict_n["Expanded academy"], building_dict_n["Academy of Light"], building_dict_n["Academy of Dark"], building_dict_n["Academy of Abjuration"], building_dict_n["Academy of Destruction"], building_dict_n["Academy of Daemonic"], building_dict_n["Academy of Necromancy"]]
		
		# First we want a list of all our cities
		our_city_list = []
		their_city_list = []
		
		failures = []
		for city_id, the_city in city_dict_c.items():
			if the_city.dead > 0: continue
			
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			else:
				their_city_list.append(city_id)
		
		# New we compare each with each
		for our_city_id in our_city_list:
			our_city = city_dict_c[our_city_id]
			
			for their_city_id in their_city_list:
				their_city = city_dict_c[their_city_id]
				
				# Is this city within range?
				distance = data.path.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance <= 150:
					# Check for Expanded or Specialist
					city_buildings = their_city.get_buildings()[1]
					
					for b in academy_type_list:
						if b in city_buildings and city_buildings[b] > 0:
							failures.append(their_city.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Negative:</span> No cities within 150 map units of your have an expanded/specialist academy in them")
			return favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Negative:</span> The following cities have an expanded/specialist academy in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Negative:</span> The city of %s has an expanded/specialist academy in it" % (failures[0]))
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Phraela_and_Caist(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: All cities are within 100 map units of at least two of your other cities
	#------------------------
	def major():
		city_dict	= the_world.cities()
		failures	= []
		
		for city_id_1, the_city_1 in city_dict.items():
			if the_city_1.team != the_team.id or the_city_1.dead: continue
			cities_within_range = 0
			
			for city_id_2, the_city_2 in city_dict.items():
				if the_city_2.team != the_team.id or the_city_2.dead: continue
				if city_id_2 == city_id_1: continue
				
				distance = path_f.pythagoras((the_city_1.x, the_city_1.y), (the_city_2.x, the_city_2.y))
				
				if distance <= 150:
					cities_within_range += 1
			
			if cities_within_range < 2:
				failures.append(the_city_1.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Major:</span> All of your cities are within 150 units of at least two other of your cities")
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following cities are not within 150 units of at least two other of your cities: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> The city of %s not within 150 map units of at least two of your other cities" % (failures[0]))
			return favour_rewards["major_neg"]
	
	#	Minor: You have a city within 150 map units of another Phraela and Caist follower or 3 of your own
	#------------------------
	def minor():
		city_dict		= the_world.cities()
		team_dict		= the_world.teams()
		deities_lookup	= the_world.deities_lookup()
		
		city_success = False
		for k, our_city in city_dict.items():
			if city_success: continue
			
			self_success = 0
			
			# We only want to use our own cities thanks, nor will we use our dead cities for this test
			if our_city.team != the_team.id: continue
			if our_city.dead: continue
			
			for k, their_city in city_dict.items():
				if city_success: continue# This one has passed already
				
				# If they don't follow P&C we don't care
				if deities_lookup['Phraela and Caist'] not in team_dict[their_city.team].get_deities(the_world.cursor):
					continue
				
				if their_city.dead: continue# Ignore dead cities
				
				distance = path_f.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				# Success?
				if distance < 150:
					if their_city.team == the_team.id:
						# It's us, we need at least 3 in total
						self_success += 1
						if self_success >= 3: city_success = True
					else:
						# It's an ally, outright success
						city_success = True
		
		if city_success:
			info.append("<span class='pos'>Minor:</span> One or more of your cities are within 150 map units of another Phraela and Caist follower's city or 3 of your own cities")
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> None of your cities are within 150 map units of another Phraela and Caist follower's city nor 3 of your own cities")
			return favour_rewards["minor_neg"]
	
	#	Negative: Any of your cities are closer to a non-Phraela and Caist follower than they are to a Phraela and Caist follower or one of your own cities
	#------------------------
	def negative():
		team_dict		= the_world.teams()
		deities_lookup	= the_world.deities_lookup()
		city_dict		= the_world.cities()
		
		failures = []
		failure_details = {}
		for city_id_1, the_city_1 in city_dict.items():
			if the_city_1.team != the_team.id or the_city_1.dead == True: continue
			
			failure_details[the_city_1.name] = ''
			pac_range	= 9999999
			other_range	= 9999999
			
			for city_id_2, the_city_2 in city_dict.items():
				if the_city_2.dead == True or city_id_2 == city_id_1: continue
				
				distance = path_f.pythagoras((the_city_1.x, the_city_1.y), (the_city_2.x, the_city_2.y))
				
				if deities_lookup['Phraela and Caist'] in team_dict[the_city_2.team].get_deities(the_world.cursor):
					pac_range = min(pac_range, distance)
				else:
					if other_range > distance:
						failure_details[the_city_1.name] = the_city_2.name
						other_range = min(other_range, distance)
			
			if other_range < pac_range:
				# print the_city_1.name, " - ", failure_details[the_city_1.name], "<br />"
				failures.append(the_city_1.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Negative:</span> All of your cities are closer to one that follows Phraela and Caist than to one that does not")
			return favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Negative:</span> The following cities closer to a city that does not follow Phraela and Caist than one that does: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Negative:</span> The city of %s is closer to a city that does not follow Phraela and Caist than to one that does" % (failures[0]))
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Soag_chi(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: An operative within every non Soag chi city within 100 units of each of yours where your city and their city is at least 3 years old
	#------------------------
	def major():
		team_dict			= the_world.teams()
		deities_lookup		= the_world.deities_lookup()
		city_dict			= the_world.cities()
		operatives_from_team	= the_world.operatives_from_team(the_team.id)
		
		# We want to build a cache for our operatives in which cities
		cities_with_our_ops = []
		for o, the_op in operatives_from_team.items():
			cities_with_our_ops.append(the_op.city)
			
		cities_with_our_ops = set(cities_with_our_ops)
		
		# First we want a list of all our cities
		our_city_list = []
		their_city_list = []
		
		failures = []
		for city_id, the_city in city_dict.items():
			if the_city.dead > 0: continue
			if common.current_turn() - the_city.founded <= 3: continue
			
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			else:
				# If they follow Soag chi then we can skip them
				if deities_lookup['Soag chi'] in team_dict[the_city.team].get_deities(the_world.cursor): continue
				their_city_list.append(city_id)
		
		# New we compare each with each
		for our_city_id in our_city_list:
			our_city = city_dict[our_city_id]
			
			for their_city_id in their_city_list:
				their_city = city_dict[their_city_id]
				
				# Is this city within range?
				distance = path_f.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance <= 100:
					# Check for operative
					if their_city_id not in cities_with_our_ops:
						failures.append(their_city.name)
		
		# failures = list(set(failures))
		
		if len(failures) < 1:
			info.append("<span class='pos'>Major:</span> All cities within 100 units of one of your cities where one or both cities are older than 2 years have an operative in them")
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following foreign cities do not have operatives in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> The foreign city of %s does not have an operative in it" % (failures[0]))
			return favour_rewards["major_neg"]
	
	#	Minor: One or more of your cities are within 10 map units of a non-Soag chi follower
	#------------------------
	def minor():
		team_dict		= the_world.teams()
		deities_lookup	= the_world.deities_lookup()
		city_dict		= the_world.cities()
		
		city_in_range = False
		for city_id_1, the_city_1 in city_dict.items():
			if the_city_1.team != the_team.id or the_city_1.dead: continue
			if city_in_range: continue
			
			for city_id_2, the_city_2 in city_dict.items():
				if the_city_2.dead or city_id_2 == city_id_1: continue
				if deities_lookup['Soag chi'] in team_dict[the_city_2.team].get_deities(the_world.cursor): continue
				
				distance = path_f.pythagoras((the_city_1.x, the_city_1.y), (the_city_2.x, the_city_2.y))
				
				if distance < 50: city_in_range = True
		
		if city_in_range:
			info.append("<span class='pos'>Minor:</span> One of your cities is within 50 map units of a city that does not follow Soag chi")
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> None of your cities are within 50 map units of a city that does not follow Soag chi")
			return favour_rewards["minor_neg"]
	
	#	Negative: None of your cities are within 50 map units of a non-Soag chi follower
	#------------------------
	def negative():
		team_dict		= the_world.teams()
		deities_lookup	= the_world.deities_lookup()
		city_dict		= the_world.cities()
		
		city_in_range = False
		for city_id_1, the_city_1 in city_dict.items():
			if the_city_1.team != the_team.id or the_city_1.dead: continue
			if city_in_range: continue
			
			for city_id_2, the_city_2 in city_dict.items():
				if the_city_2.dead or city_id_2 == city_id_1: continue
				if deities_lookup['Soag chi'] in team_dict[the_city_2.team].get_deities(the_world.cursor): continue
				
				distance = path_f.pythagoras((the_city_1.x, the_city_1.y), (the_city_2.x, the_city_2.y))
				
				if distance < 50:
					city_in_range = True
		
		if city_in_range:
			info.append("<span class='pos'>Negative:</span> You have at least one city within 50 map units of a city that does not follow Soag chi")
			return favour_rewards["negative_pos"]
		else:
			info.append("<span class='neg'>Negative:</span> None of your cities are within 50 map units of a city that does not follow Soag chi")
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Khystrik(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: All cities are nomadic
	#------------------------
	def major():
		city_dict_c		= city.get_city_dict_c()
		failures		= []
		
		for city_id, the_city in city_dict_c.items():
			if the_city.team != the_team.id or the_city.dead: continue
			
			if not the_city.nomadic:
				failures.append(the_city.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Major:</span> All your cities are nomadic")
			return favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Major:</span> The following cities are not nomadic: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Major:</span> The city of %s is not nomadic" % (failures[0]))
			return favour_rewards["major_neg"]
	
	#	Minor: No cities older than 2 years within 100 units of any of your cities
	#------------------------
	def minor():
		team_dict_c			= data.team.get_teams_dict_c()
		deity_dict_n		= data.deity.get_deity_dict_n()
		city_dict_c			= city.get_city_dict_c()
		operatives_by_city	= operative.get_operatives_by_city()
		operatives_dict_c	= operative.get_operatives_dict_c()
		
		# First we want a list of all our cities
		# our_city_list = [c.id for c in city_dict_c.itervalues() if c.team == the_team.id and c.dead == False]
		our_city_list = []
		their_city_list = []
		
		failures = []
		for city_id, the_city in city_dict_c.items():
			if the_city.dead > 0: continue
			if common.current_turn() - the_city.founded <= 3: continue
			
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			else:
				# If they follow Soag chi then we can skip them
				if deity_dict_n['Soag chi'] in team_dict_c[the_city.team].get_deities(): continue
				their_city_list.append(city_id)
		
		# New we compare each with each
		for our_city_id in our_city_list:
			city_fails = False
			our_city = city_dict_c[our_city_id]
			
			for their_city_id in their_city_list:
				if city_fails: continue
				their_city = city_dict_c[their_city_id]
				
				# Is this city within range?
				distance = data.path.pythagoras((our_city.x, our_city.y), (their_city.x, their_city.y))
				
				if distance <= 100:
					if common.current_turn() - their_city.founded > 2:
						city_fails = True
						failures.append(our_city.name)
		
		if len(failures) < 1:
			info.append("<span class='pos'>Minor:</span> All your cities are at least 100 units away from any city older than 2 years")
			return favour_rewards["minor_pos"]
		else:
			if len(failures) > 1:
				info.append("<span class='neg'>Minor:</span> The following cities are within 100 map units of one or more cities older than 2 years: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				info.append("<span class='neg'>Minor:</span> The city of %s is within 100 map units of a city older than two years" % (failures[0]))
			return favour_rewards["minor_neg"]
	
	#	Negative: None of your cities are nomadic
	#------------------------
	def negative():
		city_dict_c		= city.get_city_dict_c()
		none_nomadic	= True
		
		for city_id, the_city in city_dict_c.items():
			if the_city.team != the_team.id or the_city.dead: continue
			
			if the_city.nomadic:
				none_nomadic = False
		
		if none_nomadic:
			info.append("<span class='pos'>Negative:</span> At least one of your cities are nomadic")
			return favour_rewards["negative_pos"]
		else:
			info.append("<span class='neg'>Negative:</span> None of your cities are nomadic")
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Laegus(the_world, the_team):
	favour = 0
	info = []
	
	#	Major: Ended the turn with fewer than 100 materials
	#------------------------
	def major():
		# If this is in pre-orders then the stats won't exist
		# If it's mid-turn the stats are what we need
		if common.current_turn() in the_team.get_stats(the_world.cursor):
			team_stats = the_team.get_stats(the_world.cursor)[common.current_turn()]
			materials = res_dict.Res_dict(team_stats.resources).get("Materials")
		else:
			materials = res_dict.Res_dict(the_team.resources).get("Materials")
		
		if materials <= 100:
			info.append("<span class='pos'>Major:</span> You ended the year with fewer than 100 surplus materials")
			return favour_rewards["major_pos"]
		else:
			info.append("<span class='neg'>Major:</span> You ended the year with a surplus of over 100 materials (%s)" % materials)
			return favour_rewards["major_neg"]
	
	#	Minor: Army is at least 15% the size of your population
	#------------------------
	def minor():
		army_size = team_q.get_unit_category_size(the_world.cursor, the_team.id, 0, 100)
		pop_size	= the_team.get_population(the_world.cursor)
		
		if pop_size == 0:
			army_percent = 100
		else:
			army_percent = int((float(army_size)/float(pop_size))*100)
		if army_percent >= 15:
			info.append("<span class='pos'>Minor:</span> Your armed forces are at least 15%% the size of your population (%s%%)" % (army_percent))
			return favour_rewards["minor_pos"]
		else:
			info.append("<span class='neg'>Minor:</span> Your armed forces are less than 15%% the size of your population (currently %s%%)" % (army_percent))
			return favour_rewards["minor_neg"]
	
	#	Negative: Participated in more than 1 war
	#------------------------
	def negative():
		if campaign_f.team_campaign_count(the_world.cursor, the_team.id, common.current_turn()) <= 1:
			info.append("<span class='pos'>Negative:</span> You participated in no more than one war last year")
			return favour_rewards["negative_pos"]
		else:
			info.append("<span class='neg'>Negative:</span> You participated in more than one war last year")
			return favour_rewards["negative_neg"]
	
	favour += major()
	favour += minor()
	favour += negative()
	
	return favour, "<br />".join(info)

def Zasha(the_world, the_team):
	favour = 0
	info = []
	
	return favour, "<br />".join(info)

def Alki(the_world, the_team):
	favour = 0
	info = []
	
	return favour, "<br />".join(info)


deity_favour = {
	"Arl":					Arl,
	"Trchkithin":			Trchkithin,
	"Adyl":					Adyl,
	"Ssai":					Ssai,
	"Orakt":				Orakt,
	"Agashn":				Agashn,
	"Ldura":				Ldura,
	"Azmodius":				Azmodius,
	"Phraela and Caist":	Phraela_and_Caist,
	"Soag chi":				Soag_chi,
	"Khystrik":				Khystrik,
	"Laegus":				Laegus,
	"Zasha":				Zasha,
	"Alki":					Alki
}


def calculate_favour(cursor, the_world, the_team, deity_ref):
	"""Deity_ref can be the name or id"""
	deity_dict = the_world.deities()
	deity_lookup = the_world.deities_lookup(lower=True)
	
	# If we're sent a name then we need to find the deity
	if type(deity_ref) == str:
		if deity_ref in deity_lookup:
			deity_ref = deity_lookup[deity_ref]
	
	if deity_ref in deity_dict:
		the_deity = deity_dict[deity_ref]
	else:
		raise Exception("No deity of name '%s'" % deity_ref)
	
	if the_deity.name not in deity_favour:
		return 0, "Error: No deity function of the name %s in rules.deity_favour.calculate_favour(%s, %s)\n" % (name, the_team.id, deity_ref)
	
	return deity_favour[the_deity.name](the_world, the_team)


