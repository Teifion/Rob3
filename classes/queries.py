import re
import database


subjects = (
	# 0 - Nothing
	"No subject",
	
	# 01 - Team stuff
	"Edit team",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	
	# 10 - City stuff
	"Edit city",
	"Growing cities",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	
	# 20 - Orders stuff
	"Normal orders",
	"Trades",
	"Requests",
	"Partial orders",
	"Pre orders resources",
	"",
	"",
	"",
	"",
)

class Query (database.DB_connected_object):
	table_info = {
		"Name":			"queries",
		"Indexes":		{
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Integer_field("time"),
			database.Integer_field("turn"),
			database.Integer_field("subject"),
			
			database.Text_field("query_data"),
		),
	}
	
	def __init__(self, row = {}):
		super(Query, self).__init__(row)
	
