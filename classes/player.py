import database

daemon_types = (
	"Common",
	"Minor",
	"Shifter",
	"Hunter killer",
	
	"Midian",
	"Elemental",
	"Oiixoi",
	"Regenerator",
	
	"Legerdemain",
	"Splitter",
	"Angelic",
	"Thirster",
)

progressions = (
	"No progression",
	"Transfigured",
	"Metamorphosed",
	"Ascended",
	"Demigod",
)

class Player (database.DB_connected_object):
	table_info = {
		"Name":			"players",
		"Indexes":		{
			"name": "name",
			"team":	"team",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=40),
			
			database.Boolean_field("not_a_player"),
			database.Boolean_field("ir"),
			database.Boolean_field("not_surplus"),
			
			database.Integer_field("team",			foreign_key=("teams", "id")),
			database.Integer_field("last_posted"),
			
			database.Integer_field("daemon_type"),
			database.Integer_field("progression"),
		),
	}
	
	def __init__(self, row = {}):
		super(Player, self).__init__(row)
		# Calc'd
		self.feats	= {}
		self.kills	= {}
		self.deaths	= {}
		self.powers = [None]
	
	# def get_deaths(self, force_requery=False):
	# 	"""Sets the dictionary of our resources"""
	# 	if self.deaths != {} and force_requery == False:
	# 		return self.deaths
	# 	
	# 	self.deaths = {}
	# 	
	# 	query = "SELECT killer, turn FROM achievements WHERE victim = %d" % (self.id)
	# 	try:
	# 		database.cursor.execute(query)#TODO Use new method
	# 	except Exception as e:
	# 		print("Query: %s\n" % query)
	# 		raise e
	# 	while (1):
	# 		row = database.cursor.fetchone()
	# 		if row == None: break
	# 		self.deaths[row['killer']] = row['turn']
	# 	
	# 	return self.deaths
	
	# def get_kills(self, force_requery=False):
	# 	"""Sets the dictionary of our resources"""
	# 	if self.kills != {} and force_requery == False:
	# 		return self.kills
	# 	
	# 	self.kills = {}
	# 	
	# 	query = "SELECT victim, turn FROM achievements WHERE killer = %d" % (self.id)
	# 	try:
	# 		database.cursor.execute(query)#TODO Use new method
	# 	except Exception as e:
	# 		print("Query: %s\n" % query)
	# 		raise e
	# 	while (1):
	# 		row = database.cursor.fetchone()
	# 		if row == None: break
	# 		self.kills[row['victim']] = row['turn']
	# 	
	# 	return self.kills
	
	# def get_feats(self, force_requery=False):
	# 	"""Sets the dictionary of our resources"""
	# 	if self.feats != {} and force_requery == False:
	# 		return self.feats
	# 	
	# 	self.feats = {}
	# 
	# 	query = "SELECT feat, level FROM feats WHERE player = %d" % (self.id)
	# 	try:
	# 		database.cursor.execute(query)#TODO Use new method
	# 	except Exception as e:
	# 		print("Query: %s\n" % query)
	# 		raise e
	# 	while (1):
	# 		row = database.cursor.fetchone()
	# 		if row == None: break
	# 		self.feats[row['feat']] = row['level']
	# 
	# 	return self.feats
	
	def get_powers(self, cursor, force_requery=False):
		"""Returns a list of the power-id's that this player has"""
		if self.powers != [] and force_requery == False:
			return self.feats
		
		self.powers = []
		
		query = """SELECT id FROM powers WHERE player = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.powers.append(row['id'])
		
		return self.powers


# # Achievments (kills)
# tempLink = database.DB_link_object()
# tempLink.table_name		= "achievements"
# tempLink.primary_keys	= ["killer", "victim"]
# tempLink.indexes		= []
# tempLink.add_field('killer',	'int')
# tempLink.add_field('victim',	'int')
# tempLink.add_field('turn',		'int')
# self.link_tables.append(tempLink)		
# 
# # Feats
# tempLink = database.DB_link_object()
# tempLink.table_name		= "feats"
# tempLink.primary_keys	= ["player", "feat"]
# tempLink.indexes		= []
# tempLink.add_field('player',	'int')
# tempLink.add_field('feat',		'int')
# tempLink.add_field('level',		'int')
# self.link_tables.append(tempLink)

Player_history = {
	"Name":			"player_history",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("team",		primary_key=True, foreign_key=("teams", "id")),
		database.Integer_field("player",	primary_key=True, foreign_key=("players", "id")),
		database.Integer_field("turn"),
	),
}

Player_kills = {
	"Name":			"player_kills",
	"Indexes":		{
	},
	"Fields":		(
		database.Serial_field("id",			primary_key=True),
		database.Integer_field("killer",	foreign_key=("players", "id")),
		database.Integer_field("victim",	foreign_key=("players", "id")),
		database.Integer_field("battle"),# We want to continue to record this kill even if the battle is deleted
		database.Integer_field("turn"),
	),
}