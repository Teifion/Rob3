from classes import world
from queries import city_q, team_q, squad_q, unit_q

# Contains some special functions that are only nedeed for spy stuff so can be kept separate
class Spy_world (world.World):
	def __init__(self, cursor):
		super(Spy_world, self).__init__(cursor)
		
		# Spy specific things
		self._operatives_in_area = {}
		self._operatives_in_city = {}
		self._cities_in_area = {}
		self._armies_in_area = {}
		self._armies_by_base = {}
		self._diff_cache = {}
		
		# Prep for spy reports
		# player_q.mass_get_player_powers(self.cursor, self._players)
		# mapper_q.get_terrain(self.cursor, 0, 0)
		
		self.teams()
		# team_q.mass_get_team_deities(self.cursor, self._teams)
		# team_q.mass_get_team_spells(self.cursor, self._teams)
		team_q.mass_get_team_techs(self.cursor, self._teams)
		# team_q.mass_get_team_resources(self.cursor, self._teams)
		team_q.mass_get_team_evolutions(self.cursor, self._teams)
		
		self.buildings()
		self.cities()
		city_q.mass_get_city_buildings(self.cursor, self._cities)
		# city_q.mass_get_city_artefacts(self.cursor, self._cities)
		# city_q.mass_get_city_wonders(self.cursor, self._cities)
		
		self.armies()
		squad_q.mass_get_squads(self.cursor, self._armies)
		
		self.units()
		unit_q.mass_get_unit_equipment(self.cursor, self._units)
		
		# for k, v in self._buildings.items():
		# 	if v.upgrades > 0:
		# 		if v.upgrades not in self._building_requirements:
		# 			self._building_requirements[v.upgrades] = []
		# 		
		# 		self._building_requirements[v.upgrades].append(k)
	
	def armies_by_base(self, base, force_requery=False):
		if base in self._armies_by_base and not force_requery:
			return self._armies_by_base[base]
		
		self._armies_by_base = {}
		
		# Get all the ones for it
		self.armies()
		for i, a in self._armies.items():
			if a.base not in self._armies_by_base:
				self._armies_by_base[a.base] = []
			
			self._armies_by_base[a.base].append(i)
		
		return self._armies_by_base[base]
	
	def armies_in_area(self, area, radius=10, force_requery=False):
		if (area, radius) in self._armies_in_area and not force_requery:
			return self._armies_in_area[(area, radius)]
		
		self.cities_in_area(area, radius, force_requery)
		self._armies_in_area[(area, radius)] = []
		
		if len(self._cities_in_area[(area, radius)]) > 0:
			sql_extra = "OR garrison IN (%s)" % ",".join([str(c) for c in self._cities_in_area[(area, radius)]])
		else:
			sql_extra = ""
		
		# Get armies query
		query = """SELECT id FROM armies
			WHERE x > {minx} AND x < {maxx}
				AND y > {miny} AND y < {maxy} {sql_extra}""".format(
			minx = area[0] - radius,
			maxx = area[0] + radius,
			miny = area[1] - radius,
			maxy = area[1] + radius,
			sql_extra = sql_extra,
		)
		try: self.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in self.cursor:
			self._armies_in_area[(area, radius)].append(row['id'])
		
		return self._armies_in_area[(area, radius)]
	
	def operatives_in_area(self, area, radius=10, force_requery=False):
		if (area, radius) in self._operatives_in_area and not force_requery:
			return self._operatives_in_area[(area, radius)]
		
		self.cities_in_area(area, radius, force_requery)
		self._operatives_in_area[(area, radius)] = []
		
		if len(self._cities_in_area[(area, radius)]) == 0:
			return []
		
		# Get cities in the area
		query = """SELECT id FROM operatives
			WHERE city IN (%s)""" % ",".join([str(c) for c in self._cities_in_area[(area, radius)]])
		try: self.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in self.cursor:
			self._operatives_in_area[(area, radius)].append(row['id'])
		
		return self._operatives_in_area[(area, radius)]
	
	def operatives_in_city(self, city_id, force_requery=False):
		the_city = self.cities(force_requery)[city_id]
		
		if city_id in self._operatives_in_city and not force_requery:
			return self._operatives_in_city[city_id]
		
		self._operatives_in_city[city_id] = []
		
		# Get cities in the city
		query = """SELECT id FROM operatives
			WHERE city = %d""" % city_id
		try: self.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in self.cursor:
			self._operatives_in_city[city_id].append(row['id'])
		
		return self._operatives_in_city[city_id]
	
	def cities_in_area(self, area, radius=10, force_requery=False):
		if (area, radius) in self._cities_in_area and not force_requery:
			return self._cities_in_area[(area, radius)]
		
		self._cities_in_area[(area, radius)] = []
		
		# Get cities in the area
		query = """SELECT id FROM cities
			WHERE x > {minx} AND x < {maxx}
				AND y > {miny} AND y < {maxy}""".format(
			minx = area[0] - radius,
			maxx = area[0] + radius,
			miny = area[1] - radius,
			maxy = area[1] + radius,
		)
		try: self.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in self.cursor:
			self._cities_in_area[(area, radius)].append(row['id'])
		
		return self._cities_in_area[(area, radius)]
	
	def race_difference(self, race_1, race_2):
		"""Returns the percentage difference between two races, race_1 and 2 are both team ids"""
		# On the basis that this will be called a lot, caching is a really cunning plan I think
		if (race_1, race_2) in self._diff_cache:
			return self._diff_cache[(race_1, race_2)]
		
		if (race_2, race_1) in self._diff_cache:
			return self._diff_cache[(race_2, race_1)]
		
		# Now to start our actual work
		evolution_dict = self.evolutions()
		team_1 = self.teams()[race_1]
		team_2 = self.teams()[race_2]
		
		current_diff = 0
		for evo_id, the_evo in evolution_dict.items():
			# Default both to level 0, this stops missing key exception
			team_1.evolutions[evo_id] = team_1.evolutions.get(evo_id, 0)
			team_2.evolutions[evo_id] = team_2.evolutions.get(evo_id, 0)
			
			level_diff = abs(team_1.evolutions[evo_id] - team_2.evolutions[evo_id])
			if level_diff != 0 and the_evo.physical_change != 0:
				# print the_evo.name, ": ", the_evo.physical_change * level_diff, "<br />"
				current_diff += the_evo.physical_change * level_diff
		
		self._diff_cache[(race_1, race_2)] = current_diff
		return self._diff_cache[(race_1, race_2)]
	


