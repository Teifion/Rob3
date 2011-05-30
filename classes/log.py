import database

class Log (database.DB_connected_object):
	table_info = {
		"Name":			"logs",
		"Indexes":		{
			"turn": 	"turn",
			"team": 	"team",
			"player":	"player",
		},
		"Fields": (
			database.Serial_field("id",				primary_key = True),
			database.Integer_field("player",		default = -1),
			database.Integer_field("team",			default = -1),
			database.Integer_field("turn"),
			database.Varchar_field("tags",			max_length=40),
			
			database.Text_field("content"),
			database.Varchar_field("cost",			max_length=255),
		),
	}
	
	def __init__(self, row = {}):
		super(Log, self).__init__(row)
	
	