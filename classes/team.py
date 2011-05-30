import database
from classes import res_dict
from classes import army, stat
# from hashlib import md5
# from data import team_f, team_q
# from data import resource_f
# from data import order_post
# from rules import deity_rules
# from rules import team_rules
# from data import stat, stat_f, stat_q
# from data import army

border_states = [
	"At war",
	"Closed",
	"Segregated",
	"Open",
	"Allied",
]
default_border_state = border_states.index("Open")

def border_colour(state):
	if type(state) == int:
		state = border_states[state]
	
	if state == "At war":		return "AA0000"
	elif state == "Closed":		return "AA6600"
	elif state == "Segregated":	return "AAAA00"
	elif state == "Open":		return "0000AA"
	elif state == "Allied":		return "00AA00"
	else:
		raise Exception("No handler for the state of '%s'" % state)

class Team (database.DB_connected_object):
	table_info = {
		"Name":			"teams",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Serial_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=30),
			
			database.Integer_field("forum_url_id"),
			database.Integer_field("orders_topic"),
			database.Integer_field("intorders_topic"),
			database.Integer_field("results_topic"),
			database.Integer_field("teaminfo_topic"),
			database.Integer_field("team_info_first_post"),
			
			database.Integer_field("request_topic"),
			
			database.Integer_field("culture_topic"),
			
			database.Integer_field("leader_id"),
			
			database.Boolean_field("active"),
			database.Boolean_field("ir"),
			database.Boolean_field("dead"),
			database.Boolean_field("not_in_queue"),
			database.Boolean_field("hidden"),
			database.Boolean_field("not_a_team"),
			
			database.Integer_field("join_turn"),
			database.Integer_field("default_borders",		default=default_border_state),
			database.Integer_field("default_taxes",			default=10),
			
			database.Double_field("evo_points",				default=10),
			
			database.Varchar_field("primary_colour",		max_length=6),
			database.Varchar_field("secondary_colour",		max_length=6),
			
			# Used to store non-resetting resources from last turn
			database.Varchar_field("previous_resources"),
		),
	}
	
	def __init__(self, row = {}):
		super(Team, self).__init__(row)
		
		# Calculated properties
		self.population			= -1
		self.slaves				= -1
		self.resources			= res_dict.Res_dict()
		self.previous_dict		= res_dict.Res_dict()
		
		self.temple_points		= -1
		
		self.deities			= {"Checked":False}
		self.evolutions			= {"Checked":False}
		
		self.units				= {}
		self.artefacts			= [None]
		self.wonders			= [None]
		self.traits				= [None]
		
		self.spell_levels		= {"Checked":False}
		self.spell_points		= {"Checked":False}
		
		self.tech_levels		= {"Checked":False}
		self.tech_points		= {"Checked":False}
		
		self.relations			= {"Checked":False}
		self.stats				= {"Checked":False}
		
		self.overbudget			= []#["Materials"]
		self.research_sent		= 0
	
	def clean_name(self):
		return self.name.replace("'", '').replace(' ', '').replace('(', '').replace(')', '').lower()
	
	def get_size(self, cursor, force_requery=False):
		if force_requery == False and (self.population > -1 and self.slaves > -1):
			return (self.population + self.slaves)
		
		self.population = 0
		self.slaves = 0
		
		query = "SELECT slaves, population FROM cities WHERE team = {0:d} AND dead < 1".format(self.id)
		try:
			cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.population += row['population']
			self.slaves += row['slaves']
		
		return self.population + self.slaves
	
	def get_population(self, cursor, force_requery=False):
		if force_requery == False and self.population > -1:
			return self.population
		
		self.get_size(cursor, force_requery)
		return self.population
	
	def get_slaves(self, cursor, force_requery=False):
		if force_requery == False and self.slaves > -1:
			return self.slaves
		
		self.get_size(cursor, force_requery)
		return self.slaves
	
	def get_resources(self, cursor, force_requery=False):
		"""Sets the dictionary of our resources"""
		if self.resources.value != {} and force_requery == False:
			return self.resources
		
		temp_dict = {}
		
		query = "SELECT resource, amount FROM team_resources WHERE team = {0:d}".format(self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			temp_dict[row['resource']] = row['amount']
		
		self.resources = res_dict.Res_dict(temp_dict)
		self.temporary_resources = res_dict.Res_dict(temp_dict)
		
		return self.resources
	
	def get_spells(self, cursor, force_requery=False):
		if self.spell_levels != {"Checked":False} and force_requery == False:
			return self.spell_levels, self.spell_points
		
		self.spell_levels = {}
		self.spell_points = {}
		
		query = "SELECT spell, points, level FROM team_spells WHERE team = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.spell_levels[row['spell']] = row['level']
			self.spell_points[row['spell']] = row['points']
		
		return self.spell_levels, self.spell_points
	
	def get_techs(self, cursor, force_requery=False):
		if self.tech_levels != {"Checked":False} and force_requery == False:
			return self.tech_levels, self.tech_points
		
		self.tech_levels = {}
		self.tech_points = {}
		
		query = "SELECT tech, points, level FROM team_techs WHERE team = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.tech_levels[row['tech']] = row['level']
			self.tech_points[row['tech']] = row['points']
		
		return self.tech_levels, self.tech_points
	
	def get_deities(self, cursor, force_requery=False):
		"""Sets the dictionary of our resources"""
		if self.deities != {"Checked":False} and force_requery == False:
			return self.deities
		
		self.deities = {}
		
		query = "SELECT deity, favour FROM team_deities WHERE team = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.deities[row['deity']] = row['favour']
		
		return self.deities
	
	def get_evolutions(self, cursor, force_requery=False):
		"""Sets the dictionary of our evolutions"""
		if self.evolutions != {"Checked":False} and force_requery == False:
			return self.evolutions
		
		self.evolutions = {}
		
		query = "SELECT evolution, level FROM team_evolutions WHERE team = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.evolutions[row['evolution']] = row['level']
		
		return self.evolutions
	
	def get_units(self, cursor, force_requery = False):
		"""Sets the dictionary of our units"""
		if self.units != {} and not force_requery:
			return self.units
		
		self.units = {}
		
		query = "SELECT unit, amount, army FROM squads WHERE team = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			if row['unit'] not in self.units:
				self.units[row['unit']] = 0
			
			# if row['unit'] == 628
			
			self.units[row['unit']] += row['amount']
		
		return self.units
	
	def get_orders(self, cursor, the_world, order_type, turn):
		from classes import order_post
		
		if order_type == "normal":
			query = """SELECT * FROM orders
				WHERE turn = %d AND topic = %d ORDER BY post_id ASC""" % (turn, self.orders_topic)
		
		elif order_type == "international":
			query = """SELECT * FROM orders
				WHERE turn = %d AND topic = %d ORDER BY post_id ASC""" % (turn, self.intorders_topic)
		
		else:
			raise Exception("Error in data.team.Team.get_orders(), an order_type of '%s' was passed, no handler for it." % order_type)
			exit()
		
		the_orders = []
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			the_orders.append(order_post.Order_post(the_world, row))
			the_orders[-1].team_ref = self
		
		return the_orders
	
	def get_stats(self, cursor, force_requery=False):
		"""Gets all the stats for this team"""
		if self.stats != {"Checked":False} and not force_requery:
			return self.stats
		
		self.stats = {}
		
		query = "SELECT * FROM team_stats WHERE team = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.stats[row['turn']] = stat.Stat(row)
		
		return self.stats
	
	def get_artefacts(self, cursor, force_requery=False):
		if self.artefacts != [None] and not force_requery:
			return self.artefacts
		
		self.artefacts = []
		
		query = """SELECT id FROM artefacts WHERE team = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.artefacts.append(row['id'])
		
		return self.artefacts
	
	def get_wonders(self, cursor, force_requery=False):
		if self.wonders != [None] and not force_requery:
			return self.wonders
		
		self.wonders = []
		
		query = """SELECT id FROM wonders WHERE team = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.wonders.append(row['id'])
		
		return self.wonders
	
	def get_traits(self, cursor, force_requery = False):
		if self.traits != [None] and not force_requery:
			return self.traits
		
		self.traits = []
		
		query = """SELECT trait FROM team_traits WHERE team = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.traits.append(row['trait'])
		
		return self.traits
	
	# def resource_needed(self, resource_name):
	# 	"""Returns the amount of a given resource needed by that team"""
	# 	return team_rules.resource_needed(resource_name, self)
	
	def operative_count(self, cursor):
		"""Returns the number of operatives that the team has"""
		count = 0
		query = """SELECT size FROM operatives WHERE team = %d AND died < 1""" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			count += row['size']
		
		return count
	
	# def get_borders(self, force_requery=False):
	# 	"""docstring for get_borders"""
	# 	if self.borders != {"Checked":False} and force_requery == False:
	# 		return self.borders
	# 	
	# 	self.borders = {}
	# 	
	# 	query = """SELECT visitor, state FROM team_borders WHERE host = %d""" % self.id
	# 	try: database.cursor.execute(query)
	# 	except Exception as e:
	# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	# 	for row in database.cursor:
	# 		self.borders[row['visitor']] = row['state']
	# 	
	# 	return self.borders

Team_resources = {
	"Name":			"team_resources",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("resource",		primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
		
		database.Double_field("amount"),
	),
}

Team_relations = {
	"Name":			"team_relations",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("host",			primary_key=True, foreign_key=("teams","id")),
		database.Integer_field("visitor",		primary_key=True, foreign_key=("teams","id")),
		
		database.Integer_field("border",		default=-1),
		database.Double_field("taxes",			default=-1),# Rate in %
	),
}

Border_history = {
	"Name":			"border_history",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("host",			primary_key=True),
		database.Integer_field("visitor",		primary_key=True),
		
		database.Integer_field("state"),
	),
}

Team_deities = {
	"Name":			"team_deities",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("deity",			primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
		
		database.Integer_field("favour"),
	),
}

Team_evolutions = {
	"Name":			"team_evolutions",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("evolution",		primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
		
		database.Integer_field("level"),
	),
}

Team_spells = {
	"Name":			"team_spells",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("spell",			primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
		
		database.Integer_field("level"),
		database.Integer_field("points"),
	),
}

Team_techs = {
	"Name":			"team_techs",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("tech",			primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
		
		database.Integer_field("level"),
		database.Integer_field("points"),
	),
}

Team_json_ti = {
	"Name":			"team_json_ti",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("turn",			primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
		
		database.Text_field("content"),
	),
}

Team_traits = {
	"Name":			"team_traits",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("trait",			primary_key=True),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams","id")),
	),
}