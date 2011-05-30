import database

class Turn (database.DB_connected_object):
	table_info = {
		"Name":			"turns",
		"Indexes":		{
		},
		"Fields":		(
			database.Integer_field("turn",			primary_key=True),
			database.Integer_field("turn_time"),
		),
	}
	
	def __init__(self, row = {}):
		super(Turn, self).__init__(row)
