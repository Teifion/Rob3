import database

# operative_types = {0: ""}

class Operative (database.DB_connected_object):
	table_info = {
		"Name":			"operatives",
		"Indexes":		{
			"city": "city",
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			database.Integer_field("city",			foreign_key=("cities", "id")),
			
			database.Varchar_field("name",			max_length=30),
			database.Integer_field("arrival"),
			database.Integer_field("died",			default=0),
			database.Integer_field("size",			default=1),
			
			database.Integer_field("stealth",		default=1),
			database.Integer_field("observation",	default=1),
			database.Integer_field("integration",	default=1),
			database.Integer_field("sedition"),
			database.Integer_field("sabotage"),
			database.Integer_field("assassination"),
		),
	}
	
	def __init__(self, row = {}):
		super(Operative, self).__init__(row)