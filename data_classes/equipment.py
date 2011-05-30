import database
from rules import map_data

cat_list = [
	'Training', 

	'Sword',
	'Axe',
	'Hammer',
	'Flail',
	'Polearm',
	'Dagger',

	'Bow',
	'Crossbow',
	'Thrown',
	'Gunpowder',

	'Armour',
	'Shield',

	'Mount',
	'Seabourne mount',
	'Beast',

	'Siege engine',
	'Boat hull',
	'Balloon',

	'Custom',
]

damage_list = [
	"Blunt",
	"Pierce",
	"Slash",

	# Combos
	"Blunt/Slash",
	"Blunt/Pierce",
	"Pierce/Slash",

	# Very versatile!
	"Blunt/Pierce/Slash",
]

speed_list = [
	"Slow",
	"Average",
	"Fast",
]

move_type = [
	"Foot",
	"Mule",
	"Horse",	
	"Sail",
	"Balloon",
	"Wing",
]

move_speed = [
	"March",
	"Ride",
	"Sail",
	"Fly",
]


class Equipment (database.DB_connected_object):
	table_info = {
		"Name":			"equipment_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",				primary_key=True),
			database.Varchar_field("name",				max_length=40),
			
			database.Varchar_field("cost",				max_length=255),
			database.Varchar_field("cost_multiplier",	max_length=255),
			
			database.Varchar_field("upkeep",			max_length=255),
			database.Varchar_field("upkeep_multiplier",	max_length=255),
			
			database.Text_field("description"),
			database.Integer_field("category"),
			
			database.Integer_field("crew"),
			database.Integer_field("transport"),
			database.Boolean_field("large_transport"),
			
			database.Integer_field("grep_priority"),
			database.Boolean_field("public"),
			
			# Limiters
			database.Integer_field("continent"),
			database.Integer_field("terrain"),
			database.Integer_field("tech"),
			database.Integer_field("tech_level"),
			
			# Category stats
			database.Integer_field("move_speed"),
			database.Integer_field("move_type"),
			
			database.Integer_field("armour_cat"),
			database.Integer_field("move_cat"),
			database.Integer_field("training_cat"),
			
			# Combat stats
			database.Integer_field("damage_type"),
			database.Double_field("range"),
			database.Boolean_field("one_handed"),
			database.Boolean_field("two_handed"),
			
			database.Double_field("weight"),
			database.Integer_field("speed"),
		),
	}
	
	def __init__(self, row = {}):
		super(Equipment, self).__init__(row)
