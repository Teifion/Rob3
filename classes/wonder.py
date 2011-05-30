import database

class Wonder (database.DB_connected_object):
	table_info = {
		"Name":			"wonders",
		"Indexes":		{
			"city": "city",
			# "team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=60),
			
			database.Integer_field("city",			foreign_key=("cities", "id")),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			database.Boolean_field("completed"),
			database.Integer_field("completion"),
			database.Integer_field("point_cost"),
			database.Integer_field("material_cost"),
			database.Text_field("description"),
		),
	}
	
	def __init__(self, row = {}):
		super(Wonder, self).__init__(row)