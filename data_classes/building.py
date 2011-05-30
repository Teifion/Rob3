import database

class Building (database.DB_connected_object):
	table_info = {
		"Name":			"building_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=30),
			
			database.Integer_field("build_time"),
			database.Integer_field("upgrades"),
			database.Boolean_field("has_upgrade"),
			database.Boolean_field("wall"),
			database.Boolean_field("economy"),
			database.Boolean_field("needs_port"),
			database.Boolean_field("public"),
			
			database.Varchar_field("cost_per_turn",	max_length=50),
			database.Varchar_field("cost_up_front",	max_length=50),
			database.Varchar_field("upkeep",		max_length=50),
			
			database.Integer_field("limit_per_city"),
			
			database.Varchar_field("description",		max_length=255),
		),
	}
	
	def __init__(self, row = {}):
		super(Building, self).__init__(row)