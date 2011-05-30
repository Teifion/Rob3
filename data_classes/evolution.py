import database

categories = [
	'Physical',
	'Mental',
	'Affinity',
	'Radical',
]

class Evolution (database.DB_connected_object):
	table_info = {
		"Name":			"evolution_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=40),
			
			
			database.Integer_field("cost_per_level"),
			database.Integer_field("max_level"),
			database.Integer_field("min_level"),
			database.Integer_field("category"),
			
			database.Double_field("physical_change"),
			database.Boolean_field("combat_relevant"),
			
			database.Text_field("description"),
		),
	}
	
	def __init__(self, row = {}):
		super(Evolution, self).__init__(row)