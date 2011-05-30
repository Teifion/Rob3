import database

category = {
	"none":		1,
	"common":	2,
	"one off":	3,
}

class Tech (database.DB_connected_object):
	table_info = {
		"Name":			"tech_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=40),
			
			database.Varchar_field("base_cost",		max_length=255),
			database.Varchar_field("extra_cost",	max_length=255),
			
			database.Integer_field("max_level"),
			database.Integer_field("category"),
			
			database.Boolean_field("tradable"),
			
			database.Text_field("description"),
		),
	}
	
	def __init__(self, row = {}):
		super(Tech, self).__init__(row)