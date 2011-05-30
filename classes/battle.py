import database
import re

battle_coords = re.compile(r"(-?[0-9]*), ?(-?[0-9]*)")

battle_types = (
	"None",
	
	"Ambush",
	"Pitched",
	"Skimishes",
	"Siege",
	
	"Sabotage",
)

result_types = (
	"None",
	
	"Decisive victory to attacker",
	"Victory to attacker",
	"Pyrrhic victory to attacker",
	"Undecided",
	"Pyrrhic victory to defender",
	"Victory to defender",
	"Decisive victory to defender",
)

class Battle (database.DB_connected_object):
	table_info = {
		"Name":			"battles",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=60),
			database.Integer_field("campaign",		foreign_key=("campaigns", "id")),
			database.Integer_field("city"),
			database.Integer_field("start"),
			database.Integer_field("duration"),# In days
			database.Integer_field("type"),
			database.Integer_field("result"),
			
			database.Integer_field("x"),
			database.Integer_field("y"),
		),
	}
	
	def __init__(self, row = {}):
		super(Battle, self).__init__(row)
		
		# Cacl'd fields
		self.losses	= {}
		self.armies	= []
		self.squads	= []	
	
	def get_from_form(self, form_list):
		super(Battle, self).get_from_form(form_list)
		
		for http_data in form_list:
			if http_data.name == "location":
				location = battle_coords.search(http_data.value).groups()
				self.x = location[0]
				self.y = location[1]
	
	def get_armies(self, cursor, force_requery):
		if force_requery == False and self.armies != []:
			return self.armies
		self.armies = []
		
		query = """SELECT army
			FROM campaign_armies
				WHERE campaign = {c}
				AND started <= {start}
				AND (finished >= {start} OR finished = 0)""".format(
				c = self.campaign,
				start = self.start,
			)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.armies.append(str(row['army']))
		
		return self.armies
	
	def get_squads(self, cursor, force_requery=False):
		if force_requery == False and self.squads != []:
			return self.squads
		self.squads = []
		
		self.get_armies(cursor, force_requery)
		
		if self.armies == []:
			return []
		
		query = "SELECT id FROM squads WHERE army in ({0})".format(",".join([str(a) for a in self.armies]))
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.squads.append(row['id'])
		
		return self.squads
	
	def get_losses(self, cursor, force_requery=False):
		"""Gets all the participants of the war"""
		if force_requery == False and self.losses != {}:
			return self.losses
		self.losses = {}
		
		query = """SELECT squad, losses FROM squad_battle_history WHERE battle = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.losses[row['squad']] = row['losses']
		
		return self.losses