import database

class Deity (database.DB_connected_object):
	table_info = {
		"Name":			"deity_list",
		"Indexes":		{
			"name": "name",
		},
		"Fields":		(
			database.Integer_field("id",			primary_key=True),
			database.Varchar_field("name",			max_length=40),
			database.Varchar_field("sname",			max_length=7),
			
			database.Text_field("major"),
			database.Text_field("minor"),
			database.Text_field("negative"),
			database.Boolean_field("monotheistic"),
			
			database.Text_field("bonus"),
			database.Text_field("objective"),
			database.Text_field("di"),
			database.Text_field("summary"),
			database.Text_field("backstory"),
			
			database.Text_field("likes"),
			database.Text_field("dislikes"),
			database.Text_field("hates"),
		),
	}
	
	def __init__(self, row = {}):
		super(Deity, self).__init__(row)
		
		# Custom fields
		self.favour_items						= []# A list of functions