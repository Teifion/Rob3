import warnings
from pages import common
from classes import res_dict, team
from queries import team_q, city_q, ti_q, player_q, battle_q, campaign_q
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

class Deity (object):
	def __init__(self, the_world):
		super(Deity, self).__init__()
		self.w = the_world
		
		self.favour = 0
		self.info = []
	
	def major(self, the_team): warnings.warn("Not implimented", RuntimeWarning)
	def minor(self, the_team): warnings.warn("Not implimented", RuntimeWarning)
	def negative(self, the_team): warnings.warn("Not implimented", RuntimeWarning)
	def other(self, the_team): warnings.warn("Not implimented", RuntimeWarning)

class Arl (Deity):
	#	Major: End the turn with at least 1 more city than you started it with
	#------------------------
	def major(self, the_team):
		try:
			cities_this_turn = the_team.stats[common.current_turn()].city_count
		except Exception:
			cities_this_turn = 0
		
		if (common.current_turn()-1) not in the_team.stats:
			cities_last_turn = 0
		else:
			cities_last_turn = the_team.stats[common.current_turn()-1].city_count
		
		if cities_this_turn > cities_last_turn:
			self.info.append("<span class='pos'>Major:</span> You have at least 1 more city this turn than the last")
			self.favour += favour_rewards["major_pos"]
		else:
			self.info.append("<span class='neg'>Major:</span> You do not have at least 1 more city this turn than the last")
			self.favour += favour_rewards["major_neg"]
	
	
	#	Minor: All of your cities are within 100 units of another nation's city
	#------------------------
	def minor(self, the_team):
		our_cities = self.w.live_cities_from_team(the_team.id)
		city_dict = self.w.live_cities()
		
		failures = []
		for k, our_city in our_cities.items():
			city_is_within_range = False
			
			for k, their_city in city_dict.items():
				if city_is_within_range: continue# We've approved this one already
				if their_city.team == the_team.id: continue# Ignore ourselves
				
				distance = path_f.pythagoras(our_city, their_city)
				if distance < 100:
					city_is_within_range = True
			
			if not city_is_within_range:
				failures.append(our_city.name)
		
		if len(failures) == 0:
			self.info.append("<span class='pos'>Minor:</span> All of your cities are within 100 units of a city from another nation")
			self.favour += favour_rewards["minor_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Minor:</span> The following cities are not within 100 units of a city from another nation: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Minor:</span> The city %s is not within 100 units of a city from another nation" % (failures[0]))
			self.favour += favour_rewards["minor_neg"]
			
	
	#	Negative: At least as many civilians as last turn
	#------------------------
	def negative(self, the_team):
		try:
			pop_this_turn = the_team.stats[common.current_turn()].population
		except Exception:
			pop_this_turn = 250
		
		if (common.current_turn()-1) not in the_team.stats:
			pop_last_turn = 250
		else:
			pop_last_turn = the_team.stats[common.current_turn()-1].population
		
		if pop_this_turn > pop_last_turn:
			self.info.append("<span class='pos'>Negative:</span> You have at least as many civilians as last turn")
			self.favour += favour_rewards["negative_pos"]
		else:
			self.info.append("<span class='neg'>Negative:</span> You have fewer civilians than you did last turn")
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass
	


class Trchkithin (Deity):
	#	Major: Trchkithin nations control at least 40% of the chosen land
	#------------------------
	def major(self, the_team):
		team_dict		= self.w.active_teams()
		deities_lookup	= self.w.deities_lookup()
		
		total_control = 0
		trch_control = 0
		for team_id, the_team in team_dict.items():
			if the_team.ir: continue
			
			if common.current_turn() in the_team.stats:
				if deities_lookup['Trchkithin'] in the_team.get_deities(self.w.cursor):
					trch_control += the_team.stats[common.current_turn()].land_controlled
				
				total_control += the_team.stats[common.current_turn()].land_controlled
		
		if total_control == 0:
			trch_control_percent = 0
		else:
			trch_control_percent = round(100*trch_control/float(total_control), 2)
		
		# Add 5 for the temple
		city_dict		= self.w.cities()
		wonders_lookup	= self.w.wonders_lookup()
		wonder_id		= wonders_lookup.get('Palace of Trchkithin', -1)
		
		if wonder_id > 0:
			the_wonder = self.w.wonders()[wonder_id]
			if the_wonder.city in city_dict and city_dict[the_wonder.city].dead < 1:
				trch_control_percent += 5
		
		if trch_control_percent >= 40:
			self.info.append("<span class='pos'>Major:</span> Trchkithin nations control over 40%% of the land controlled by Chosen ones (%s%%)" % (trch_control_percent))
			
			self.favour += favour_rewards["major_pos"]
		else:
			self.info.append("<span class='neg'>Major:</span> Trchkithin nations control less than 40%% of the land controlled by Chosen ones (%s%%)" % (trch_control_percent))
			
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: Your slave count is at least 20% the size of your population
	#------------------------
	def minor(self, the_team):
		slave_size	= the_team.get_slaves(self.w.cursor)
		pop_size	= the_team.get_population(self.w.cursor)
		
		# Prevent divide by 0 rubbish
		pop_size = max(pop_size, 1)
		slave_percent = int(100*slave_size/pop_size)
		if slave_percent > 20:
			self.info.append("<span class='pos'>Minor:</span> You have at least 1 slave for every 5 people (%s%%)" % (slave_percent))
			self.favour += favour_rewards["minor_pos"]
		else:
			if slave_size == 0:
				self.info.append("<span class='neg'>Minor:</span> You have no slaves, you need at least 1 for every 5 people (%s)" % (pop_size/5.0))
			elif slave_size == 1:
				self.info.append("<span class='neg'>Minor:</span> You have only one slave, you need at least 1 for every 5 people (%s)" % (pop_size/5.0))
			else:
				self.info.append("<span class='neg'>Minor:</span> You have only %s slaves (need at least %s)" % (slave_size, pop_size/5.0))
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: A city within 200 map units follows Arl
	#------------------------
	def negative(self, the_team):
		city_dict		= self.w.live_cities()
		our_cities		= self.w.live_cities_from_team(the_team.id)
		team_dict		= self.w.active_teams()
		deities_lookup	= self.w.deities_lookup()
		
		failures = []
		for k, our_city in our_cities.items():
			city_failure = ""
			
			for k, their_city in city_dict.items():
				if city_failure != "": continue# We've failed this one already
				if deities_lookup['Arl'] not in team_dict[their_city.team].get_deities(self.w.cursor): continue
				
				if their_city.team == the_team.id: continue# Ignore ourselves
				
				distance = path_f.pythagoras(our_city, their_city)
				
				if distance < 200:
					city_failure = their_city.name
					failures.append((our_city.name, city_failure))
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Negative:</span> No Arl aligned cities are within 200 units of any of your cities")
			self.favour += favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Negative:</span> The following cities are within 200 units of an Arl aligned city: %s and %s" % (
					", ".join(["%s (%s)" % (a,b) for a, b in failures[0:-1]]),# ", ".join(failures[0:-1]),
					"%s (%s)" % failures[-1]
				))
			else:
				self.info.append("<span class='neg'>Negative:</span> The city of %s is within 200 units of one or more Arl aligned cities (%s)" % (failures[0]))
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		wonders_lookup = self.w.wonders_lookup()
		
		if wonders_lookup['Palace of Trchkithin'] in the_team.get_wonders(self.w.cursor):
			self.info.append("<span class='pos'>Palace of Trchkithin:</span> +1 favour from the Palace of Trchkithin")
			self.favour += 1


class Adyl (Deity):
	#	Major: All cities of 30k or more must are walled
	#------------------------
	def major(self, the_team):
		city_dict		= self.w.live_cities()
		our_cities		= self.w.cities_from_team(the_team.id)
		
		failures = []
		for k, our_city in our_cities.items():
			if our_city.size >= 20000:
				if len(our_city.walled(self.w.cursor)) < 1:
					failures.append(our_city.name)
		
		if len(failures) == 0:
			self.info.append("<span class='pos'>Major:</span> All of your cities larger than 20k people are walled")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following cities are larger than 20,000 people and not walled: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> Your city of %s is larger than 20,000 people is not walled")
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: Participated in a war
	#------------------------
	def minor(self, the_team):
		if campaign_f.team_campaign_count(self.w.cursor, the_team.id, common.current_turn()) > 0:
			self.info.append("<span class='pos'>Minor:</span> You participated in at least one war")
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> You did not participate in any wars")
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: A city of 30k or larger is not walled
	#------------------------
	def negative(self, the_team):
		our_cities		= self.w.cities_from_team(the_team.id)
		team_dict		= self.w.active_teams()
		
		failures = []
		for k, our_city in our_cities.items():
			if our_city.size >= 30000:
				if len(our_city.walled(self.w.cursor)) < 1:
					failures.append(our_city.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Negative:</span> All cities larger than 30,000 have a wall")
			self.favour += favour_rewards["negative_pos"]
		else:
			if len(failures) == 1:
				self.info.append("<span class='neg'>Negative:</span> The city of %s has no wall" % (failures[0]))
			else:
				self.info.append("<span class='neg'>Negative:</span> The following cities have no wall: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass

class Ssai (Deity):
	#	Major: Must have an operative within every non-allied nation that has a city within 1000 units of one of yours
	#------------------------
	def major(self, the_team):
		team_dict		= self.w.active_teams()
		city_dict		= self.w.live_cities()
		our_cities		= self.w.cities_from_team(the_team.id)
		operatives_dict	= self.w.operatives_from_team(the_team.id)
		relations		= self.w.relations()
		
		# Build our cachelist
		operatives_by_city = {}
		for o, the_op in operatives_dict.items():
			if the_op.died > 0: continue
			if the_op.city not in operatives_by_city: operatives_by_city[the_op.city] = []
			operatives_by_city[the_op.city].append(o)
		
		nations_in_range = set()
		nations_infiltrated = set()
		non_allied_nations = []
		
		# Get a list of non-allied nations
		for other_id, other_team in team_dict.items():
			if other_id != the_team.id:
				if relations.get(the_team.id, {}).get(other_id, {}).get('border', other_team.default_borders) < team.border_states.index("Allied"):
					non_allied_nations.append(other_id)
		
		# Now for a list of cities we are in range of
		for other_id, other_city in city_dict.items():
			if other_city.team not in non_allied_nations:# This includes ourselves, we're not a non-allied nation to ourselves
				continue
			
			# We have already got a spy in one of their cities
			if other_city.team in nations_infiltrated:
				continue
			
			for our_id, our_city in our_cities.items():
				# Is this city within range?				
				if path_f.pythagoras(our_city, other_city) <= 1000:
					# Add it to the list of nations in range
					nations_in_range.add(other_city.team)
					
					if other_id in operatives_by_city:
						nations_infiltrated.add(other_city.team)
		
		# Now to find out what nations we fail at
		failures = []
		for t in nations_in_range:
			if t not in nations_infiltrated:
				failures.append(team_dict[t].name)
		
		if len(failures) == 0:
			self.info.append("<span class='pos'>Major:</span> You have operatives within all nations within 1000 units of your cities")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following nations do not have operatives in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> The nation of %s does not have an operative in it" % (failures[0]))
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: At least 1 operative per 1000 troops
	#------------------------
	def minor(self, the_team):
		squad_dict		= self.w.squads_from_team(the_team.id)
		operatives_dict	= self.w.operatives_from_team(the_team.id)
		
		army_size	= sum([s.amount for i, s in squad_dict.items()])
		op_count	= sum([(o.size if o.died < 1 else 0) for i, o in operatives_dict.items()])
		
		if army_size == 0:	op_ratio = 1
		else:				op_ratio = round(op_count*1000/army_size, 2)
		
		if op_ratio >= 1:
			self.info.append("<span class='pos'>Minor:</span> You have at least 1 spy per 1000 troops (%s per 1000)" % (op_ratio))
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> You have fewer than 1 spy per 1000 troops (%s per 1000)" % (op_ratio))
			self.favour += favour_rewards["minor_neg"]
			
	
	#	Negative: A non-allied city within 100 units of one of yours is over 2 years old and is not infiltrated
	#------------------------
	def negative(self, the_team):
		team_dict		= self.w.active_teams()
		city_dict		= self.w.live_cities()
		our_cities		= self.w.cities_from_team(the_team.id)
		operatives_dict	= self.w.operatives_from_team(the_team.id)
		relations		= self.w.relations()
		
		non_allied_nations = []
		
		# Build our cachelist
		operatives_by_city = {}
		for o, the_op in operatives_dict.items():
			if the_op.died > 0: continue
			if the_op.city not in operatives_by_city: operatives_by_city[the_op.city] = []
			operatives_by_city[the_op.city].append(o)
		
		# Get a list of non-allied nations
		for other_id, other_team in team_dict.items():
			if other_id != the_team.id:
				if relations.get(the_team.id, {}).get(other_id, {}).get('border', other_team.default_borders) < team.border_states.index("Allied"):
					non_allied_nations.append(other_id)
		
		failures = []
		# Now for a list of cities we are in range of
		for other_id, other_city in city_dict.items():
			if other_city.team not in non_allied_nations:# This includes ourselves, we're not a non-allied nation to ourselves
				continue
			
			if other_city.founded >= common.current_turn() - 2: continue# Too young
			
			city_checked = False
			for our_id, our_city in our_cities.items():
				if city_checked: continue# We already know it's a failure
				
				# Is this city within range?
				if path_f.pythagoras(our_city, other_city) <= 100:
					city_checked = True
					if other_id not in operatives_by_city:
						failures.append(other_city.name)
		
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Negative:</span> All cities older than 2 years and within 100 units of one of your cities have an operative in them")
			self.favour += favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Negative:</span> The following foreign cities do not have operatives in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Negative:</span> The foreign city of %s does not have an operative in it" % (failures[0]))
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass


class Orakt (Deity):
	#	Major: Upkeep is at least 25% of your income
	#------------------------
	def major(self, the_team):
		upkeep = team_f.get_upkeep(the_team, self.w)
		income = team_rules.produce_resources(self.w.cursor, the_team, self.w)[0].get("Materials")
		
		if income == 0:
			percentage = 100
		else:
			percentage = round(upkeep/float(income)*100, 2)
		
		if income <= (upkeep * 4):
			self.info.append("<span class='pos'>Major:</span> Your military upkeep is at least 25%% of your income (%s%%)" % percentage)
			self.favour += favour_rewards["major_pos"]
		else:
			self.info.append("<span class='neg'>Major:</span> Your military upkeep is less that 25%% of your income (%s%%)" % percentage)
			self.favour += favour_rewards["major_neg"]
		
	
	#	Minor: Participated in at least 3 wars this turn
	#------------------------
	def minor(self, the_team):
		if campaign_f.team_campaign_count(self.w.cursor, the_team.id, common.current_turn()) > 1:
			self.info.append("<span class='pos'>Minor:</span> You participated in at least two wars")
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> You participated in fewer than two wars this year")
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: Participated in 0 wars
	#------------------------
	def negative(self, the_team):
		if campaign_f.team_campaign_count(self.w.cursor, the_team.id, common.current_turn()) > 0:
			self.info.append("<span class='pos'>Negative:</span> You participated in one or more wars")
			self.favour += favour_rewards["negative_pos"]
		else:
			self.info.append("<span class='neg'>Negative:</span> You participated in no wars")
			self.favour += favour_rewards["negative_neg"]

	def other(self, the_team):
		pass


class Agashn (Deity):
	#	Major: Above average land control
	#------------------------
	def major(self, the_team):
		team_dict		= self.w.active_teams()
		
		total_control = 0
		our_control = 0
		team_count = 0
		for team_id, t in team_dict.items():
			if t.ir: continue
			
			if common.current_turn() in t.stats:
				total_control += t.stats[common.current_turn()].land_controlled
			
			team_count += 1
			
			if t.id == the_team.id:
				if common.current_turn() in t.stats:
					our_control = t.stats[common.current_turn()].land_controlled
				else:
					our_control = 0#t.stats[common.current_turn()].land_controlled
		
		average_control = total_control/team_count
		
		if average_control <= our_control:
			self.info.append("<span class='pos'>Major:</span> You have above average land control of %s, average is %s" % (our_control, average_control))
			self.favour += favour_rewards["major_pos"]
		else:
			self.info.append("<span class='neg'>Major:</span> You have below average land control of %s, average is %s" % (our_control, average_control))
			self.favour += favour_rewards["major_neg"]
			
	
	#	Minor: Army is at least 15% the size of your population
	#------------------------
	def minor(self, the_team):
		army_size = sum([s.amount for i, s in self.w.squads_from_team(the_team.id).items()])
		pop_size	= the_team.get_population(self.w.cursor)
		
		if pop_size == 0:
			army_percent = 100
		else:
			army_percent = int(army_size/pop_size*100)
		if army_percent >= 15:
			self.info.append("<span class='pos'>Minor:</span> Your armed forces are at least 15%% the size of your population (%s%%)" % (army_percent))
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> Your armed forces are less than 15%% the size of your population (currently %s, need at least %s)" % (army_size, int(pop_size/5)))
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: End the turn with fewer cities than you started with
	#------------------------
	def negative(self, the_team):
		try:
			cities_this_turn = the_team.stats[common.current_turn()].city_count
		except Exception:
			cities_this_turn = 0
		
		if (common.current_turn()-1) not in the_team.stats:
			cities_last_turn = 0
		else:
			cities_last_turn = the_team.stats[common.current_turn()-1].city_count
		
		if cities_this_turn >= cities_last_turn:
			self.info.append("<span class='pos'>Negative:</span> You have ended this year with at least as many cities as you ended last year with")
			self.favour += favour_rewards["negative_pos"]
		else:
			self.info.append("<span class='neg'>Negative:</span> You have ended this year with 1 or more fewer cities than last year")
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass


class Ldura (Deity):
	#	Major: All cities larger than 50k have an expanded university and expanded academy
	#------------------------
	def major(self, the_team):
		city_dict		= self.w.live_cities_from_team(the_team.id)
		team_dict		= self.w.active_teams()
		building_lookup	= self.w.buildings_lookup()
		
		failures = []
		for city_id, the_city in city_dict.items():
			if the_city.nomadic: continue
			
			if the_city.size >= 50000:
				city_buildings, city_buildings_amount = the_city.get_buildings(self.w.cursor)
				
				if building_lookup["Expanded academy"] not in city_buildings_amount or \
					building_lookup["Expanded university"] not in city_buildings_amount:
					failures.append(the_city.name)
		
		if len(failures) == 0:
			self.info.append("<span class='pos'>Major:</span> All of your cities larger than 50,000 people possess both an expanded academy and university")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following cities are larger than 50,000 people and not in possession of an expanded academy and university: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> Your city of %s is larger than 50,000 people is not in possession of an expanded acadamy and university" % failures[0])
			self.favour += favour_rewards["major_neg"]
		
	
	#	Minor: Every city has a university and an academy before anything else except walls
	#------------------------
	def minor(self, the_team):
		city_dict		= self.w.live_cities_from_team(the_team.id)
		team_dict		= self.w.active_teams()
		building_lookup	= self.w.buildings_lookup()
		building_dict	= self.w.buildings()
		
		academy_type_list = [building_lookup["Academy"], building_lookup["Expanded academy"], building_lookup["Academy of Light"], building_lookup["Academy of Dark"], building_lookup["Academy of Abjuration"], building_lookup["Academy of Destruction"], building_lookup["Academy of Daemonic"], building_lookup["Academy of Necromancy"]]
		university_type_list = [building_lookup["University"], building_lookup["Expanded university"]]
		
		failures = []
		for city_id, the_city in city_dict.items():
			if the_city.nomadic: continue
			
			city_buildings, city_buildings_amount = the_city.get_buildings(self.w.cursor)
			
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
			self.info.append("<span class='pos'>Minor:</span> All of your cities have an academy and a university or no other buildings")
			self.favour += favour_rewards["minor_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following cities do not have an academy and university but do have other buildings: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> Your city of %s has no academy and university but does have other buildings" % failures[0])
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: Participated in more than 1 war
	#------------------------
	def negative(self, the_team):
		if campaign_f.team_campaign_count(self.w.cursor, the_team.id, common.current_turn()) > 1:
			self.info.append("<span class='neg'>Negative:</span> You participated in more than one war this year")
			self.favour += favour_rewards["negative_neg"]
		else:
			self.info.append("<span class='pos'>Negative:</span> You participated in one or fewer wars this year")
			self.favour += favour_rewards["negative_pos"]
	
	def other(self, the_team):
		pass


class Azmodius (Deity):
	#	Major: You have no mages
	#------------------------
	def major(self, the_team):
		unit_dict			= self.w.units()
		equipment_lookup	= self.w.equipment_lookup()
		squad_dict			= self.w.squads_from_team(the_team.id)
		
		failures = []
		magic_units = [1,2,3,4,5,6,7,8,9]# Default mages
		for unit_id, the_unit in unit_dict.items():
			if the_unit.team != the_team.id: continue
			
			unit_equipment = the_unit.get_equipment(self.w.cursor)
			if equipment_lookup["Low tier magic"] in unit_equipment or \
				equipment_lookup["Mid tier magic"] in unit_equipment or \
				equipment_lookup["High tier magic"] in unit_equipment:
				magic_units.append(unit_id)
		
		for squad_id, the_squad in squad_dict.items():
			if the_squad.amount < 1: continue
			
			if the_squad.unit in magic_units:
				failures.append(the_squad.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Major:</span> You have no mages")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Negative:</span> You have mages in the following squads: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Negative:</span> The squad of %s has mages in it" % (failures[0]))
			
			self.favour += favour_rewards["negative_pos"]
	
	#	Minor: Your army is at least 20% the size of your population (yes it's the same as Agashn)
	#------------------------
	def minor(self, the_team):
		army_size = sum([s.amount for i, s in self.w.squads_from_team(the_team.id).items()])
		pop_size	= the_team.get_population(self.w.cursor)
		
		if pop_size == 0:
			army_percent = 100
		else:
			army_percent = int(army_size/pop_size*100)
		if army_percent >= 20:
			self.info.append("<span class='pos'>Minor:</span> Your armed forces are at least 20%% the size of your population (%s%%)" % (army_percent))
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> Your armed forces are less than 20%% the size of your population (currently %s, need at least %s)" % (army_size, pop_size/5))
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: A city within 150 units of one of yours has an expanded or specialised academy
	#------------------------
	def negative(self, the_team):
		team_dict		= self.w.active_teams()
		city_dict		= self.w.live_cities()
		building_lookup	= self.w.buildings_lookup()
		
		# Might need to get the buildings for each city
		need_lookup = False
		for k, v in city_dict.items():
			if v.buildings == {"0":None}:
				need_lookup = True
		if need_lookup:	
			city_q.mass_get_city_buildings(self.w.cursor, self.w._cities)
		
		academy_type_list = [building_lookup["Expanded academy"], building_lookup["Academy of Light"], building_lookup["Academy of Dark"], building_lookup["Academy of Abjuration"], building_lookup["Academy of Destruction"], building_lookup["Academy of Daemonic"], building_lookup["Academy of Necromancy"]]
		
		# First we want a list of all our cities
		our_city_list = []
		their_city_list = []
		
		failures = []
		for city_id, the_city in city_dict.items():
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			else:
				their_city_list.append(city_id)
		
		# New we compare each with each
		for our_city_id in our_city_list:
			our_city = city_dict[our_city_id]
			
			for their_city_id in their_city_list:
				their_city = city_dict[their_city_id]
				
				# Is this city within range?
				distance = path_f.pythagoras(our_city, their_city)
				
				if distance <= 150:
					# Check for Expanded or Specialist
					city_buildings = their_city.get_buildings(self.w.cursor)[1]
					
					for b in academy_type_list:
						if b in city_buildings and city_buildings[b] > 0:
							failures.append(their_city.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Negative:</span> No cities within 150 map units of your have an expanded/specialist academy in them")
			self.favour += favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Negative:</span> The following cities have an expanded/specialist academy in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Negative:</span> The city of %s has an expanded/specialist academy in it" % (failures[0]))
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass


class Phraela_and_Caist (Deity):
	#	Major: All cities are within 100 map units of at least two of your other cities
	#------------------------
	def major(self, the_team):
		city_dict	= self.w.live_cities_from_team(the_team.id)
		failures	= []
		
		for city_id_1, the_city_1 in city_dict.items():
			cities_within_range = 0
			
			for city_id_2, the_city_2 in city_dict.items():
				if city_id_2 == city_id_1: continue
				
				distance = path_f.pythagoras(the_city_1, the_city_2)
				
				if distance <= 150:
					cities_within_range += 1
			
			if cities_within_range < 2:
				failures.append(the_city_1.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Major:</span> All of your cities are within 150 units of at least two other of your cities")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following cities are not within 150 units of at least two other of your cities: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> The city of %s not within 150 map units of at least two of your other cities" % (failures[0]))
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: You have a city within 150 map units of another Phraela and Caist follower or 3 of your own
	#------------------------
	def minor(self, the_team):
		city_dict		= self.w.live_cities()
		team_dict		= self.w.active_teams()
		deities_lookup	= self.w.deities_lookup()
		
		city_success = False
		for k, our_city in city_dict.items():
			if city_success: continue
			
			self_success = 0
			
			# We only want to use our own cities thanks, nor will we use our dead cities for this test
			if our_city.team != the_team.id: continue
			
			for k, their_city in city_dict.items():
				if city_success: continue# This one has passed already
				
				# If they don't follow P&C we don't care
				if deities_lookup['Phraela and Caist'] not in team_dict[their_city.team].get_deities(self.w.cursor):
					continue
				
				distance = path_f.pythagoras(our_city, their_city)
				
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
			self.info.append("<span class='pos'>Minor:</span> One or more of your cities are within 150 map units of another Phraela and Caist follower's city or 3 of your own cities")
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> None of your cities are within 150 map units of another Phraela and Caist follower's city nor 3 of your own cities")
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: Any of your cities are closer to a non-Phraela and Caist follower than they are to a Phraela and Caist follower or one of your own cities
	#------------------------
	def negative(self, the_team):
		team_dict		= self.w.active_teams()
		deities_lookup	= self.w.deities_lookup()
		city_dict		= self.w.live_cities()
		
		failures = []
		failure_details = {}
		for city_id_1, the_city_1 in city_dict.items():
			if the_city_1.team != the_team.id or the_city_1.dead > 0: continue
			
			failure_details[the_city_1.name] = ''
			pac_range	= 9999999
			other_range	= 9999999
			
			for city_id_2, the_city_2 in city_dict.items():
				if the_city_2.dead > 0 or city_id_2 == city_id_1: continue
				
				distance = path_f.pythagoras((the_city_1.x, the_city_1.y), (the_city_2.x, the_city_2.y))
				
				if deities_lookup['Phraela and Caist'] in team_dict[the_city_2.team].get_deities(self.w.cursor):
					pac_range = min(pac_range, distance)
				else:
					if other_range > distance:
						failure_details[the_city_1.name] = the_city_2.name
						other_range = min(other_range, distance)
			
			if other_range < pac_range:
				# print the_city_1.name, " - ", failure_details[the_city_1.name], "<br />"
				failures.append(the_city_1.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Negative:</span> All of your cities are closer to one that follows Phraela and Caist than to one that does not")
			self.favour += favour_rewards["negative_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Negative:</span> The following cities closer to a city that does not follow Phraela and Caist than one that does: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Negative:</span> The city of %s is closer to a city that does not follow Phraela and Caist than to one that does" % (failures[0]))
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass


class Soag_chi (Deity):
	#	Major: An operative within every non Soag chi city within 100 units of each of yours where your city and their city is at least 3 years old
	#------------------------
	def major(self, the_team):
		team_dict				= self.w.active_teams()
		deities_lookup			= self.w.deities_lookup()
		city_dict				= self.w.live_cities()
		operatives_from_team	= self.w.operatives_from_team(the_team.id)
		
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
			if common.current_turn() - the_city.founded <= 3: continue
			
			if the_city.team == the_team.id:
				our_city_list.append(city_id)
			else:
				# If they follow Soag chi then we can skip them
				if deities_lookup['Soag chi'] in team_dict[the_city.team].get_deities(self.w.cursor): continue
				their_city_list.append(city_id)
		
		# Now we compare each with each
		for our_city_id in our_city_list:
			our_city = city_dict[our_city_id]
			
			for their_city_id in their_city_list:
				their_city = city_dict[their_city_id]
				
				# Is this city within range?
				distance = path_f.pythagoras(our_city, their_city)
				
				if distance <= 100:
					# Check for operative
					if their_city_id not in cities_with_our_ops:
						failures.append(their_city.name)
		
		# failures = list(set(failures))
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Major:</span> All cities within 100 units of one of your cities where one or both cities are older than 2 years have an operative in them")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following foreign cities do not have operatives in them: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> The foreign city of %s does not have an operative in it" % (failures[0]))
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: One or more of your cities are within 50 map units of a non-Soag chi follower
	#------------------------
	def minor(self, the_team):
		team_dict		= self.w.active_teams()
		deities_lookup	= self.w.deities_lookup()
		city_dict		= self.w.live_cities()
		our_cities		= self.w.live_cities_from_team(the_team.id)
		
		city_in_range = False
		for city_id_1, the_city_1 in our_cities.items():
			if city_in_range: continue
			
			for city_id_2, the_city_2 in city_dict.items():
				if city_id_2 == city_id_1: continue
				if deities_lookup['Soag chi'] in team_dict[the_city_2.team].get_deities(self.w.cursor): continue
				
				distance = path_f.pythagoras(the_city_1, the_city_2)
				
				if distance < 50: city_in_range = True
		
		if city_in_range:
			self.info.append("<span class='pos'>Minor:</span> One of your cities is within 50 map units of a city that does not follow Soag chi")
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> None of your cities are within 50 map units of a city that does not follow Soag chi")
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: None of your cities are within 50 map units of a non-Soag chi follower
	#------------------------
	def negative(self, the_team):
		team_dict		= self.w.active_teams()
		deities_lookup	= self.w.deities_lookup()
		city_dict		= self.w.live_cities()
		
		city_in_range = False
		for city_id_1, the_city_1 in city_dict.items():
			if the_city_1.team != the_team.id: continue
			if city_in_range: continue
			
			for city_id_2, the_city_2 in city_dict.items():
				if city_id_2 == city_id_1: continue
				if deities_lookup['Soag chi'] in team_dict[the_city_2.team].get_deities(self.w.cursor): continue
				
				distance = path_f.pythagoras(the_city_1, the_city_2)
				
				if distance < 50:
					city_in_range = True
		
		if city_in_range:
			self.info.append("<span class='pos'>Negative:</span> You have at least one city within 50 map units of a city that does not follow Soag chi")
			self.favour += favour_rewards["negative_pos"]
		else:
			self.info.append("<span class='neg'>Negative:</span> None of your cities are within 50 map units of a city that does not follow Soag chi")
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass
	


class Khystrik (Deity):
	#	Major: All cities are nomadic
	#------------------------
	def major(self, the_team):
		city_dict		= self.w.live_cities_from_team(the_team.id)
		failures		= []
		
		for city_id, the_city in city_dict.items():
			if not the_city.nomadic:
				failures.append(the_city.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Major:</span> All your cities are nomadic")
			self.favour += favour_rewards["major_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Major:</span> The following cities are not nomadic: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Major:</span> The city of %s is not nomadic" % (failures[0]))
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: None of your cities are within 40 map units of each other
	#------------------------
	def minor(self, the_team):
		city_dict		= self.w.live_cities_from_team(the_team.id)
		failures = []
		
		# First we want a list of all our cities
		for c1, the_city1 in city_dict.items():
			failed = False
			for c2, the_city2 in city_dict.items():
				if failed: continue
				if c1 == c2: continue
				
				distance = path_f.pythagoras(the_city1, the_city2)
				
				if distance < 40:
					failed = True
					failures.append(the_city1.name)
		
		if len(failures) < 1:
			self.info.append("<span class='pos'>Minor:</span> All your cities are at least 100 units away from any city older than 2 years")
			self.favour += favour_rewards["minor_pos"]
		else:
			if len(failures) > 1:
				self.info.append("<span class='neg'>Minor:</span> The following cities are within 100 map units of one or more cities older than 2 years: %s and %s" % (", ".join(failures[0:-1]), failures[-1]))
			else:
				self.info.append("<span class='neg'>Minor:</span> The city of %s is within 100 map units of a city older than two years" % (failures[0]))
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: None of your cities are nomadic
	#------------------------
	def negative(self, the_team):
		city_dict		= self.w.live_cities_from_team(the_team.id)
		one_nomadic		= False
		
		for city_id, the_city in city_dict.items():
			if the_city.nomadic:
				one_nomadic = True
		
		if one_nomadic:
			self.info.append("<span class='pos'>Negative:</span> At least one of your cities are nomadic")
			self.favour += favour_rewards["negative_pos"]
		else:
			self.info.append("<span class='neg'>Negative:</span> None of your cities are nomadic")
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass



class Laegus (Deity):
	#	Major: Ended the turn with fewer than 100 materials
	#------------------------
	def major(self, the_team):
		# If this is in pre-orders then the stats won't exist
		# If it's mid-turn the stats are what we need
		try:
			materials = res_dict.Res_dict(the_team.stats[common.current_turn()].resources).get("Materials")
		except Exception:
			materials = res_dict.Res_dict(the_team.resources).get("Materials")
		
		if materials <= 100:
			self.info.append("<span class='pos'>Major:</span> You ended the year with fewer than 100 surplus materials")
			self.favour += favour_rewards["major_pos"]
		else:
			self.info.append("<span class='neg'>Major:</span> You ended the year with a surplus of over 100 materials (%s)" % materials)
			self.favour += favour_rewards["major_neg"]
	
	#	Minor: Army is at least 15% the size of your population (identical to Agashn)
	#------------------------
	def minor(self, the_team):
		army_size = sum([s.amount for i, s in self.w.squads_from_team(the_team.id).items()])
		pop_size	= the_team.get_population(self.w.cursor)
		
		if pop_size == 0:
			army_percent = 100
		else:
			army_percent = int(army_size/pop_size*100)
		if army_percent >= 15:
			self.info.append("<span class='pos'>Minor:</span> Your armed forces are at least 15%% the size of your population (%s%%)" % (army_percent))
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> Your armed forces are less than 15%% the size of your population (currently %s%%)" % (army_percent))
			self.favour += favour_rewards["minor_neg"]
	
	#	Negative: Participated in more than 1 war
	#------------------------
	def negative(self, the_team):
		if campaign_f.team_campaign_count(self.w.cursor, the_team.id, common.current_turn()) <= 1:
			self.info.append("<span class='pos'>Negative:</span> You participated in no more than one war last year")
			self.favour += favour_rewards["negative_pos"]
		else:
			self.info.append("<span class='neg'>Negative:</span> You participated in more than one war last year")
			self.favour += favour_rewards["negative_neg"]
	
	def other(self, the_team):
		pass


class Zasha (Deity):
	def major(self, the_team):
		pass
	
	def minor(self, the_team):
		pass
	
	def negative(self, the_team):
		pass
	
	def other(self, the_team):
		pass

class Alki (Deity):
	#	Major: Publically destroy a temple to a deity other than Alki using your army
	#------------------------
	def major(self, the_team):
		# Now go through the dead list and find out if any died from our army actions
		team_dict			= self.w.active_teams()
		buildings_lookup	= self.w.buildings_lookup()
		deity_lookup		= self.w.deities_lookup()
		city_dict			= self.w.live_cities(the_team.id)
		
		jsons = self.w.json_tis_from_turn(common.current_turn()-1)
		
		self.w.mass_get_city_buildings()
		self.w.mass_get_team_deities()
		
		# Get a list of all teams that don't follow Alki
		team_list = []
		for t, v in team_dict.items():
			if deity_lookup['Alki'] not in v.deities and v.deities != {} and t != the_team.id:
				team_list.append(t)
				# jsons.append(self.w.json_ti(t, common.current_turn()-1))
		
		# First get a list of all cities from last turn with a temple in them from teams
		city_list = []
		temple, expanded_temple = str(buildings_lookup['Temple']), str(buildings_lookup['Expanded temple'])
		
		for t, j in jsons.items():
			if 'cities' not in j: continue
			for c, the_city in j['cities'].items():
				buildings = the_city['buildings']
				
				if temple in buildings and buildings[temple]['completed'] > 0:
					city_list.append(int(c))
				elif expanded_temple in buildings and buildings[expanded_temple]['completed'] > 0:
					city_list.append(int(c))
				elif expanded_temple in buildings and buildings[expanded_temple]['current_progress'] > 0:
					city_list.append(int(c))
		
		# Now go through the cities and find out if any are no longer with us
		dead_list = []
		for c in city_list:
			# Not in live dict
			if c not in city_dict:
				dead_list.append(c)
			
			# In live dict but dead (how?)
			elif city_dict[c].dead > 0:
				dead_list.append(c)
			
			# In live dict but without a temple
			else:
				if city_dict[c].buildings_amount.get(buildings_lookup['Temple'], 0) <= 0 and city_dict[c].buildings_amount.get(buildings_lookup['Expanded temple'], 0) <= 0:
					dead_list.append(c)
		
		# Now we find out how many of these were in battles
		kill_list = []
		campaign_dict = campaign_q.get_campaigns_from_team(self.w.cursor, the_team.id, include_secret=True, since_turn=common.current_turn())
		campaign_list = list(campaign_dict.keys())
		
		battle_dict = battle_q.get_battles_from_turn(self.w.cursor, common.current_turn())
		for k, v in battle_dict.items():
			if v.campaign in campaign_list:
				if v.city in dead_list:
					kill_list.append(v.city)
		
		if kill_list != []:
			if len(kill_list) > 1:
				self.info.append("<span class='pos'>Major:</span> You have destroyed %d temples to deities other than Alki this year" % (len(kill_list)))
			else:
				self.info.append("<span class='pos'>Major:</span> You have destroyed 1 temple to deities other than Alki this year")
			self.favour += favour_rewards["major_pos"]
		else:
			self.info.append("<span class='neg'>Major:</span> You have destroyed no temples to deities other than Alki this year")
			self.favour += favour_rewards["major_neg"]
		
	
	#	Minor: Kill at least one non-Alki chosen this turn
	#------------------------
	def minor(self, the_team):
		team_dict		= self.w.teams()
		player_dict		= self.w.players()
		tplayer_dict	= self.w.players_from_team(the_team.id)
		deities_lookup	= self.w.deities_lookup()
		kills			= player_q.get_kills(self.w.cursor, player_dict.keys())
		
		team_players = list(tplayer_dict.keys())
		
		turn = common.current_turn()
		passes = []
		for kill in kills:
			if kill['killer'] in team_players and kill['turn'] == turn:
				team = team_dict[player_dict[kill['victim']].team]
				if deities_lookup['Alki'] not in team.get_deities(self.w.cursor) and len(team.get_deities(self.w.cursor)) > 0:
					passes.append(player_dict[kill['victim']].name)
		
		if len(passes) > 0:
			if len(passes) == 1:
				self.info.append("<span class='pos'>Minor:</span> You have slain 1 follower of another deity this turn (%s)" % (passes[0]))
			else:
				self.info.append("<span class='pos'>Minor:</span> You have slain %d followers of other deities this turn (%s and %s)" % (len(passes), ", ".join(passes[0:-1]), passes[-1]))
			self.favour += favour_rewards["minor_pos"]
		else:
			self.info.append("<span class='neg'>Minor:</span> You have slain 0 followers of the other deities")
			self.favour += favour_rewards["minor_neg"]
		
	
	#	Negative: End the turn with less temples than you started it with
	#------------------------
	def negative(self, the_team):
		buildings_lookup	= self.w.buildings_lookup()
		city_dict			= self.w.live_cities_from_team(the_team.id)
		self.w.mass_get_city_buildings()
		self.w.mass_get_team_deities()
		
		# Might need to get the buildings for each city
		need_lookup = False
		for k, v in city_dict.items():
			if v.buildings == {"0":None}:
				need_lookup = True
		if need_lookup:	
			city_q.mass_get_city_buildings(self.w.cursor, self.w._cities)
		
		temples_this_turn = 0
		for k, c in city_dict.items():
			if buildings_lookup['Temple'] in c.buildings_amount and c.buildings_amount[buildings_lookup['Temple']] > 0:
				temples_this_turn += c.buildings_amount[buildings_lookup['Temple']]
			
			if buildings_lookup['Expanded temple'] in c.buildings_amount and c.buildings_amount[buildings_lookup['Expanded temple']] > 0:
				temples_this_turn += c.buildings_amount[buildings_lookup['Expanded temple']]
		
		temples_last_turn = 0
		last_json = self.w.json_ti(the_team.id, common.current_turn()-1)
		
		# last_json = self.w.json_ti(the_team.id, common.current_turn())
		
		if last_json != {}:
			for i, c in last_json['cities'].items():
				# print(c['buildings'], "<br />")
				for i2, b in c['buildings'].items():
					if i2 == str(buildings_lookup['Temple']) and b['completed'] > 0:
						temples_last_turn += 1
					
					if i2 == str(buildings_lookup['Expanded temple']) and b['completed'] > 0:
						temples_last_turn += 1
		
		if temples_this_turn < temples_last_turn:
			self.info.append("<span class='neg'>Negative:</span> You have %d fewer temples than last turn" % (temples_last_turn - temples_this_turn))
			self.favour += favour_rewards["negative_neg"]
		else:
			self.info.append("<span class='pos'>Negative:</span> You have at least as many temples as last turn")
			self.favour += favour_rewards["negative_pos"]
	
	def other(self, the_team):
		pass


deity_instances = {
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
	"Alki":					Alki,
}

def calculate_favour(the_world, the_team, deity_ref):
	"""Deity_ref can be the name or id"""
	deity_dict = the_world.deities()
	deity_lookup = the_world.deities_lookup(lower=True)
	
	# If we're sent a name then we need to find the deity
	if type(deity_ref) == str:
		if deity_ref.lower() in deity_lookup:
			deity_ref = deity_lookup[deity_ref.lower()]
	
	# Get/Check our ref
	if deity_ref in deity_dict:
		the_deity = deity_dict[deity_ref]
	else:
		raise Exception("No deity of name '%s'" % deity_ref)
	
	# Ensure that we have a class for them
	if the_deity.name not in deity_instances:
		return 0, "Error: No deity function of the name %s in rules.deity_favour.calculate_favour(%s, %s)\n" % (name, the_team.id, deity_ref)
	
	# Create the class
	deity_instance = deity_instances[the_deity.name](the_world)
	deity_instance.major(the_team)
	deity_instance.minor(the_team)
	deity_instance.negative(the_team)
	deity_instance.other(the_team)
	
	return deity_instance.favour, "<br />".join(deity_instance.info)


