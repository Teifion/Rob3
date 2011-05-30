import database

categories = (
	"Government",
	"Religion",
	"Society",
	"Inclination",
)

class Trait (database.DB_connected_object):
	table_info = {
		"Name":			"trait_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=30),
			
			database.Integer_field("category"),
			# database.Integer_field("upgrades"),
			database.Boolean_field("show"),
			# database.Boolean_field("wall"),
			# database.Boolean_field("economy"),
			# database.Boolean_field("needs_port"),
			# database.Boolean_field("public"),
			# 
			# database.Varchar_field("cost_per_turn",	max_length=50),
			# database.Varchar_field("cost_up_front",	max_length=50),
			# database.Varchar_field("upkeep",		max_length=50),
			# 
			# database.Integer_field("limit_per_city"),
			
			database.Text_field("description",		max_length=255),
		),
	}
	
	def __init__(self, row = {}):
		super(Trait, self).__init__(row)