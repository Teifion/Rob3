import database
# from data import city

mission_states = [
	'Pending result',
	'Result given',
]

mission_types = [
	'City general',			# Target = City
	'City armies',			# Target = City
	'City buildings',		# Target = City
	'Nation morale',		# Target = Team
	'Military equipment',	# Target = Team
]

city_targets = ['City general', 'City armies', 'City buildings']
team_targets = ['Nation morale', 'Military equipment']

# Missions you probably won't get caught on
safe_missions = ['Nation morale']

mission_types_string = "|".join([m.lower() for m in mission_types])

class Mission (database.DB_connected_object):
	table_info = {
		"Name":			"missions",
		"Indexes":		{
			"turn": "turn",
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Integer_field("turn"),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			
			database.Integer_field("state"),
			database.Integer_field("time_closed"),
			database.Integer_field("time_posted"),
			
			database.Integer_field("type"),
			database.Integer_field("target"),
			
			database.Text_field("information"),
		),
	}
	
	def __init__(self, row = {}):
		super(Mission, self).__init__(row)
		
		# Calc'd fields
		self.cities		= [None]
		self.enemy_ops	= [None]
		self.allied_ops	= [None]
	
	# def get_cities(self):
	# 	"""docstring for get_cities"""
	# 	if self.cities != [None]: return self.cities
	# 	self.cities = []
	# 	
	# 	if mission_types[self.type] in city_targets:
	# 		self.cities = [self.target]
	# 	
	# 	elif mission_types[self.type] in team_targets:
	# 		query = """SELECT id, name
	# 		FROM cities
	# 			WHERE team = %d
	# 				AND dead = False""" % self.target
	# 		try: database.cursor.execute(query)
	# 		except Exception as e:
	# 			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	# 		
	# 		for row in database.cursor:
	# 			self.cities.append(row['id'])
	# 	
	# 	return self.cities
	# 
	# def get_operatives(self):
	# 	"""Gets all the operatives relative to this mission"""
	# 	if self.enemy_ops != [None]: return self.enemy_ops, self.allied_ops
	# 	self.enemy_ops, self.allied_ops = [], []
	# 	
	# 	self.get_cities()
	# 	city_list = [str(c) for c in self.cities]
	# 	
	# 	# Get target team
	# 	if mission_types[self.type] in city_targets:
	# 		city_dict_c	= city.get_city_dict_c()
	# 		target_team	= city_dict_c[self.target].team
	# 	elif mission_types[self.type] in team_targets:
	# 		target_team = self.target
	# 	
	# 	query = """SELECT id, team
	# 	FROM operatives
	# 		WHERE city in (%s)
	# 			AND died = 0""" % ",".join(city_list)
	# 	try: database.cursor.execute(query)
	# 	except Exception as e:
	# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	# 	for row in database.cursor:
	# 		if row['team'] == self.team:
	# 			self.allied_ops.append(row['id'])
	# 		elif row['team'] == target_team:
	# 			self.enemy_ops.append(row['id'])
	# 	
	# 	return self.enemy_ops, self.allied_ops


