import database

stat_tuple = (
	"population",
	"slaves",
	"resources",
	"production",
	"upkeep",
	"army_size",
	"navy_size",
	"airforce_size",
	"operatives",
	"mages",
	"land_controlled",
	"city_count",
	"war_losses",
	# "temple_count",
)

class Stat (database.DB_connected_object):
	table_info = {
		"Name":			"team_stats",
		"Indexes":		{
			"team":	"team",
		},
		"Fields":		(
			database.Integer_field("team",		primary_key=True, foreign_key=("teams", "id")),
			database.Integer_field("turn",		primary_key=True),
			
			database.Integer_field("population"),
			database.Integer_field("slaves"),
			
			database.Varchar_field("resources",	max_length=255),
			database.Varchar_field("production",	max_length=255),
			
			database.Double_field("upkeep"),
			
			database.Integer_field("army_size"),
			database.Integer_field("navy_size"),
			database.Integer_field("airforce_size"),
			
			database.Integer_field("operatives"),
			database.Integer_field("mages"),
			
			database.Double_field("land_controlled"),
			
			database.Integer_field("city_count"),
			database.Integer_field("war_losses"),
			
			# database.Integer_field("temple_count"),
		),
	}
	
	def __init__(self, row = {}):
		super(Stat, self).__init__(row)
