import database

categories = (
	'Light',
	'Dark',
	'Abjuration',
	'Destruction',
	'Daemonic',
	'Necromancy',
	'Enchantment',
	'Alchemy',
	'Animation',
	'Sourcery',
)

tiers = (
	'Low',
	'Mid',
	'High',
	'Master',
	'Ancient',
	'Epic',
)

class Spell (database.DB_connected_object):
	table_info = {
		"Name":			"spell_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=40),
			database.Integer_field("tier"),
			
			database.Integer_field("max_level"),
			database.Integer_field("category"),
			
			database.Integer_field("cooldown"),
			database.Integer_field("cast_time"),
			
			database.Boolean_field("tradable"),
			
			database.Text_field("description"),
		),
	}
	
	def __init__(self, row = {}):
		super(Spell, self).__init__(row)
	
