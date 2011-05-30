import database

power_types = (
	"Standard",
	"Reward",
)

class Power (database.DB_connected_object):
	table_info = {
		"Name":			"powers",
		"Indexes":		{
			"player": "player",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=50),
			database.Integer_field("player",		foreign_key=("players", "id")),
			database.Integer_field("type"),
			
			database.Text_field("description"),
		),
	}
	
	def __init__(self, row = {}):
		super(Power, self).__init__(row)

Power_history = {
	"Name":			"power_history",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("power",		primary_key=True, foreign_key=("powers", "id")),
		database.Integer_field("player",	primary_key=True, foreign_key=("players", "id")),
		database.Integer_field("turn"),
	),
}