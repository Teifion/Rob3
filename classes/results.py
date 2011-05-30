import database

class Result (database.DB_connected_object):
	table_info = {
		"Name":			"results_log",
		"Indexes":		{
			"turn": "turn",
			"team":	"team",
		},
		"Fields":		(
			database.Integer_field("team",		primary_key=True, foreign_key=("teams", "id")),
			database.Integer_field("turn",		primary_key=True),
			database.Boolean_field("failures",	primary_key=True),
			
			database.Text_field("content"),
		),
	}
	
	def __init__(self, row = {}):
		super(Result, self).__init__(row)
	