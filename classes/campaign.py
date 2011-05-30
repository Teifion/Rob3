import database
import re
from queries import army_q

class Campaign (database.DB_connected_object):
	table_info = {
		"Name":			"campaigns",
		"Indexes":		{
			"turn": "turn",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=60),
			database.Integer_field("turn"),
			database.Integer_field("sides",			default=2),
		),
	}
	
	def __init__(self, row = {}):
		super(Campaign, self).__init__(row)
		
		self.teams		= []
		
		self.sides_basic = {}
		self.sides_full = {}
		
		self.armies_basic = []
		self.armies_full = {}
	
	def get_sides_basic(self, cursor, force_requery=False):
		"""Gets all the participants of the war"""
		if not force_requery and self.sides_basic != {}:
			return self.sides_basic
		
		self.sides_basic = {}
		for s in range(1, self.sides+1):
			self.sides_basic[s] = []
		
		query = "SELECT side, team FROM campaign_teams WHERE campaign = %d ORDER BY side, team" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.sides_basic[row['side']].append(row['team'])
		
		return self.sides_basic
	
	def get_sides_full(self, cursor, force_requery=False):
		"""Gets all the participants of the war"""
		if not force_requery and self.sides_full != {}:
			return self.sides_full
		
		self.sides_full = {}
		for s in range(1, self.sides+1):
			self.sides_full[s] = []
		
		# Order by so that they come out in the same order each time
		query = "SELECT * FROM campaign_teams WHERE campaign = %d ORDER BY side, team" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.sides_full[row['side']].append(row)
		
		return self.sides_full
	
	def get_armies_basic(self, cursor, force_requery=False):
		"""Gets all the participants of the war"""
		if not force_requery and self.armies_basic != []:
			return self.armies_basic
		
		self.armies_basic = []
		
		query = "SELECT army FROM campaign_armies WHERE campaign = %d ORDER BY army" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.armies_basic.append(row['army'])
		
		return self.armies_basic
	
	def get_armies_full(self, cursor, force_requery=False):
		"""Gets all the participants of the war"""
		if not force_requery and self.armies_full != {}:
			return self.armies_full
		
		self.armies_full = {}
		
		# Order by so that they come out in the same order each time
		query = "SELECT * FROM campaign_armies WHERE campaign = %d ORDER BY army" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.armies_full[row['army']] = row
		
		return self.armies_full
	
	def get_armies_from_side(self, cursor, side):
		"""Return the armies used from one side"""
		
		# First we get a list of the teams on one side
		self.get_sides_basic(cursor)
		
		if side not in self.sides_basic:
			raise KeyError("%s not in self.sides_basic" % side)
		
		# Now we get a list of the armies on this side
		army_list = []
		query = """SELECT c.army
			FROM campaign_armies c, armies a
				WHERE c.campaign = {c}
				AND a.team in ({tlist})
				AND a.id = c.army""".format(
					c=self.id,
					tlist=",".join([str(t) for t in self.sides_basic[side]])
				)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			army_list.append(row['army'])
		
		return army_list
	
	def get_armies_from_team(self, cursor, team):
		"""Return the armies used from one side"""
		
		# Now we get a list of the armies from this team in this campaign
		army_list = []
		query = """SELECT c.army
			FROM campaign_armies c, armies a
				WHERE c.campaign = {c}
				AND a.team = {team}
				AND a.id = c.army""".format(
					c=self.id,
					team=team,
				)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			army_list.append(row['army'])
		
		return army_list
		

Campaign_teams = {
	"Name":			"campaign_teams",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("campaign",		primary_key=True, foreign_key=("campaigns", "id")),
		database.Integer_field("side"),
		database.Integer_field("team",			primary_key=True, foreign_key=("teams", "id")),
		# database.Integer_field("commander",		foreign_key=("players", "id")),
		
		database.Boolean_field("secret"),
		
		# When do they start and finish?
		database.Integer_field("started"),
		database.Integer_field("finished", default=360),
	),
}

Campaign_armies = {
	"Name":			"campaign_armies",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("campaign",		primary_key=True, foreign_key=("campaigns", "id")),
		database.Integer_field("army",			primary_key=True, foreign_key=("armies", "id")),
		
		# When does it enter and exit the campaign
		database.Integer_field("started"),
		database.Integer_field("finished"),
	),
}