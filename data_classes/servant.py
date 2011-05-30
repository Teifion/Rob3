import database

class Servant (database.DB_connected_object):
	table_info = {
		"Name":			"servant_list",
		"Indexes":		{
			"name": 	"name",
			"deity":	"deity",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=50),
			
			database.Integer_field("deity"),
			database.Integer_field("favour_needed"),
			database.Integer_field("temple_points"),
			database.Integer_field("summon_cost"),
			database.Integer_field("summon_amount"),
			database.Boolean_field("monotheistic"),
			
			database.Text_field("description"),
		),
	}
	def __init__(self, row = {}):
		super(Servant, self).__init__(row)