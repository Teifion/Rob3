import database

class Squad (database.DB_connected_object):
	table_info = {
		"Name":			"squads",
		"Indexes":		{
			"army": "army",
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=60),
			database.Integer_field("army",			foreign_key=("armies", "id")),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			database.Integer_field("unit",			foreign_key=("units", "id")),
			
			database.Integer_field("amount"),
			database.Integer_field("amount_at_start"),# Size at start of turn
			database.Integer_field("experience"),
		),
	}
	
	def __init__(self, row = {}):
		super(Squad, self).__init__(row)
		
		# Calc'd stuff
		self.battles	= []
		self.losses		= {}
		self.kills		= {}
			
	# def get_battles(self, force_requery=False):
	# 	"""Returns the battles we were involved in"""
	# 	if self.battles != [] and force_requery != 0:
	# 		return self.battles
	# 	
	# 	self.battles	= []
	# 	self.losses		= {}
	# 	self.kills		= {}
	# 	
	# 	query = """SELECT battle, losses, kills FROM squad_battle_history WHERE squad = %d""" % self.id
	# 	try:
	# 		database.cursor.execute(query)#TODO Use new method
	# 	except Exception as e:
	# 		print("Query: %s\n" % query)
	# 		raise e
	# 	while (1):
	# 		row = database.cursor.fetchone()
	# 		if row == None: break
	# 		self.battles.append(row['battle'])
	# 		self.losses[row['battle']] = row['losses']
	# 		self.kills[row['battle']] = row['kills']

Squad_battle_history = {
	"Name":			"squad_battle_history",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("squad",			primary_key=True, foreign_key=("squads", "id")),
		database.Integer_field("battle",		primary_key=True, foreign_key=("battles", "id")),
		
		database.Integer_field("losses"),
		database.Integer_field("kills"),
	),
}