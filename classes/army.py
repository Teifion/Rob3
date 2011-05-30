import re
import database
from queries import squad_q, monster_q
import collections

army_coords = re.compile(r"(-?[0-9]*), ?(-?[0-9]*)")

class Army (database.DB_connected_object):
	table_info = {
		"Name":			"armies",
		"Indexes":		{
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=40),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			
			database.Integer_field("x"),
			database.Integer_field("y"),
			
			database.Integer_field("old_x"),
			database.Integer_field("old_y"),
			
			# The place where they get supplies etc
			database.Integer_field("base"),
			database.Integer_field("distance"),# Distance from their base
			
			database.Integer_field("garrison",		foreign_key=("cities", "id")),
		),
	}
	
	def __init__(self, row = {}):
		super(Army, self).__init__(row)
		
		# Cacl'd fields
		self.squads = collections.OrderedDict()
		
		self.monsters		= {"Checked":False}
		self.size = -1
	
	def get_from_form(self, form_list):
		super(Army, self).get_from_form(form_list)
		
		if self.garrison == None or self.garrison < 1:
			for http_data in form_list:
				if http_data.name == "location":
					location = army_coords.search(http_data.value).groups()
					# location = re.search(r"(-?[0-9]*),(-?[0-9]*)", http_data.value).groups()
					self.x = location[0]
					self.y = location[1]
	
	def get_squads(self, cursor, force_requery=False):
		if force_requery == True or self.squads == {}:
			self.squads = squad_q.get_squads_from_army(cursor, self.id)
		
		return self.squads
	
	def get_size(self, cursor):
		if self.size >= 0:
			return self.size
		
		if len(self.squads) < 1:
			self.get_squads(cursor)
		
		self.size = 0
		for k,s in self.squads.items():
			self.size += s.amount
		
		return self.size
	
	def get_monsters(self, cursor, force_requery=False):
		if force_requery == True or self.monsters == {"Checked":False}:
			self.monsters = monster_q.get_monsters_from_army(cursor, self.id)
		
		return self.monsters

Army_monsters =  {
	"Name":			"army_monsters",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("army",		primary_key=True, foreign_key=("armies","id")),
		database.Integer_field("monster",	primary_key=True),
		
		database.Integer_field("amount"),
	),
}