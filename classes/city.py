import database
import re
import math
from rules import map_data, sad_rules
from queries import mapper_q, building_q

# from data import mapper_q
# from data import city_f, city_q
# from data import building
# 
# import data
from rules import building_rules
city_coords = re.compile(r"(-?[0-9]*), ?(-?[0-9]*)")

happiness_levels = {
	6:	"Utopian",
	5:	"Very happy",
	4:	"Very happy",
	3:	"Happy",
	2:	"Happy",
	1:	"Contented",
	0:	"Contented",
	-1:	"Unhappy",
	-2:	"Unhappy",
	-3:	"Angry",
	-4:	"Angry",
	-5:	"Utopian",
}

def happiness_str(happiness):
	if happiness not in happiness_levels:
		if happiness > 0:
			return "Utopian"
		else:
			return "Rebellious"
	
	return happiness_levels[happiness]

class City (database.DB_connected_object):
	table_info = {
		"Name":			"cities",
		"Indexes":		{
			"name": "name",
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=40),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			
			database.Integer_field("x"),
			database.Integer_field("y"),
			
			database.Integer_field("overlap"),
			
			database.Varchar_field("description",	max_length=255),
			
			database.Boolean_field("port"),
			database.Boolean_field("secret"),
			database.Boolean_field("dead_bool",		default=False),
			database.Integer_field("dead",			default=-1),
			database.Boolean_field("nomadic"),
			
			database.Integer_field("days_travelled"),
			database.Integer_field("founded"),
			
			database.Integer_field("population"),
			database.Integer_field("slaves"),
			
			# What they are making this year
			database.Integer_field("supply_good"),
			database.Integer_field("wealth"),
			database.Integer_field("supplies_satisfied"),
			database.Integer_field("happiness"),
			
			database.Integer_field("terrain"),# Used to cache terrain since it doesn't change often
			database.Varchar_field("str_supplies",	max_length=255),
		),
	}
	
	def __init__(self, row = {}):
		super(City, self).__init__(row)
		
		# Fields
		# self.add_field("goods_bonus_1",		"int")
		# self.add_field("goods_bonus_2",		"int")
		# self.add_field("goods_bonus_3",		"int")
		# self.add_field("goods_bonus_4",		"int")
		# self.add_field("goods_bonus_5",		"int")
		# self.add_field("goods_investment",	"int")
		
		self.supplies = []
		if 'str_supplies' in self.__dict__ and self.str_supplies != "":
			s_split = self.str_supplies.split(",")
			for s in s_split:
				self.supplies.append(int(s))
		
		# Supply and demand
		self.connections	= {}
		self.connections_to	= {}
		
		self.goods			= {}
		self.satisfied		= False
		self.wool_is_nice	= False
		self.temp_wealth	= self.wealth
		self.buys			= []
		self.sells			= []# Copies of the buy that has been requested
		self.needs_cache	= []
		
		# [hops][resource]
		self.best_price		= {}
		
		# Cacled
		self.buildings				= {"0":None}
		self.buildings_amount		= {"0":None}
		self.temple_points			= -999
		self.artefacts				= [None]
		self.wonders				= [None]
		self.surplus_food			= 0
		
		self.walls					= [None]
		self.size					= self.population + self.slaves
		
		self.wall_points_used		= 0
		self.building_points_used	= 0
		self.economy_points_used	= 0
		self.trade_history			= {}
	
	
	def map_link_args(self):
		return "centre={city_loc}#mv={name}".format(
			city_loc = "%s,%s" % (self.x, self.y),
			name = self.name.replace(" ", "").lower(),
		)
	
	def update(self, cursor, test_mode = False):
		super(City, self).update(cursor, test_mode)
		
		query = """UPDATE armies SET team = %d WHERE garrison = %d;""" % (int(self.team), int(self.id))
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	def point_value(self):
		val = (self.population + self.slaves)/1000
		if self.port == True:
			return (val**10)
		else:
			return (val**9)
	
	def get_from_form(self, form_list):
		super(City, self).get_from_form(form_list)
		
		for http_data in form_list:
			if http_data.name == "location":
				# location = re.search(r"(-?[0-9]*), ?(-?[0-9]*)", http_data.value).groups()
				location = city_coords.search(http_data.value).groups()
				self.x = location[0]
				self.y = location[1]
	
	def current_demands(self):
		demand_list = []
		
		# Basic
		for r in sad_rules.basic_list:
			if self.wool_is_nice and r == "Wool": continue
			elif not self.wool_is_nice and r == "Linen": continue
			if self.goods[r] < 0:
				demand_list.append(r)
		
		if demand_list != []: return demand_list
		
		# Nice
		if self.wool_is_nice and self.goods["Wool"] < 0: demand_list.append("Wool")
		elif not self.wool_is_nice and self.goods["Linen"] < 0: demand_list.append("Linen")
		
		for r in sad_rules.nice_list:
			if self.goods[r] < 0:
				demand_list.append(r)
		
		if demand_list != []: return demand_list
		
		# Luxury
		for r in sad_rules.luxury_list:
			if self.goods[r] < 0:
				demand_list.append(r)
		
		if demand_list != []: return demand_list
		
		# Exotic
		for r in sad_rules.luxury_list:
			if self.goods[r] < 0:
				demand_list.append(r)
		
		if demand_list != []: return demand_list
		
		# Satisfied!
		return demand_list
	
	def satisfaction(self):
		c = 0
		for r in sad_rules.res_list:
			if self.goods.get(r) >= 0:
				c += 1
		
		return c
	
	def walled(self, cursor, force_requery = False):
		"""Works out if the city is walled"""
		if not force_requery and self.walls != [None]:
			return self.walls
		
		self.get_buildings(cursor)
		self.walls = []
		
		building_dict = building_q.get_all_walls(cursor)
		
		for building_id, the_building in building_dict.items():
			# Complete and is a wall
			if self.buildings_amount.get(building_id, 0) >= 1:
				self.walls.append(building_id)
				continue
			
			# "Completed" but not registered as such
			if self.buildings.get(building_id, 0) >= the_building.build_time:
				self.walls.append(building_id)
				continue
			
			# What if it's an upgrade?
			if the_building.upgrades > 0 and self.buildings.get(the_building.upgrades, 0) > 0:
				self.walls.append(building_id)
				continue
		
		return self.walls
	
	# def supply(self, icon_size=-1):
	# 	if self.no_supply: return ()
	# 	if self.nomadic == 1: return 0
	# 	
	# 	if icon_size == -1:
	# 		icon_size = map_data.map_image_size(self.population+self.slaves)/2
	# 	
	# 	if self.supply_cache == None:
	# 		self.supply_cache = mapper_q.get_resource_at_x_y(self.x, self.y, icon_size)
	# 	return self.supply_cache
	
	# def supply_as_list(self, icon_size=-1):
	# 	if self.no_supply: return []
	# 	if self.nomadic == 1: return []
	# 	
	# 	if icon_size == -1:
	# 		icon_size = data.mapper.map_image_size(self.population+self.slaves)/2
	# 	
	# 	if self.supply_cache == None:
	# 		self.supply_cache = []
	# 	
	# 	return self.supply_cache
	
	def get_artefacts(self, cursor, force_requery=False):
		"""Returns the number of temple points this city has"""
		if self.artefacts != [None] and not force_requery:
			return self.artefacts
		
		self.artefacts = []
		
		query = """SELECT id FROM artefacts WHERE city = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.artefacts.append(row['id'])
		
		return self.artefacts
	
	def get_wonders(self, cursor, force_requery=False):
		"""Returns the number of temple points this city has"""
		if self.wonders != [None] and not force_requery:
			return self.wonders
		
		self.wonders = []
		
		query = """SELECT id FROM wonders WHERE city = %d""" % self.id
		try: database.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in database.cursor:
			self.wonders.append(row['id'])
		
		return self.wonders
	
	def get_temple_points(self, cursor, force_requery=False):
		if self.nomadic:
			if self.size >= 20000:
				return 1
			else:
				return 0
		
		if self.temple_points != -999 and force_requery == False:
			return self.temple_points
		
		building_completion, building_amount = self.get_buildings(cursor)
		
		temple_points = 0
		for building_id, amount in building_amount.items():
			temple_points += (building_rules.temple_points(building_id) * amount)
		
		self.temple_points = temple_points
		return self.temple_points
	
	def get_buildings(self, cursor, force_requery = False):
		if self.buildings != {"0":None} and not force_requery:
			return self.buildings, self.buildings_amount
		
		self.buildings			= {}# Progress
		self.buildings_amount	= {}# Number of buildings completed
		
		query = "SELECT building, amount, completion FROM city_buildings WHERE city = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.buildings[row['building']] = row['completion']
			self.buildings_amount[row['building']] = row['amount']
		
		return self.buildings, self.buildings_amount


City_buildings = {
	"Name":			"city_buildings",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("building",		primary_key=True),
		database.Integer_field("city",			primary_key=True, foreign_key=("cities","id")),
		
		database.Integer_field("completion"),
		database.Integer_field("amount"),
	),
}

Trade_distances =  {
	"Name":			"trade_distances",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("city_1",		primary_key=True, foreign_key=("cities","id")),
		database.Integer_field("city_2",		primary_key=True, foreign_key=("cities","id")),
		
		database.Integer_field("distance"),
	),
}