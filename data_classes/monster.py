import database

categories = (
	"Big",
	"Herded",
	"Ridden",
	"Flying"
)

class Monster (database.DB_connected_object):
	table_info = {
		"Name":			"monster_list",
		"Indexes":		{
			"name": 	"name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=50),
			database.Integer_field("category"),
			
			database.Integer_field("min_men"),
			database.Integer_field("max_men"),
			
			database.Double_field("min_budget"),
			database.Double_field("max_budget"),
			
			database.Integer_field("max_amount"),
			
			# database.Text_field("description"),
		),
	}
	
	def __init__(self, row = {}):
		super(Monster, self).__init__(row)