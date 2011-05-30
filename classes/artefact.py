import database

class Artefact (database.DB_connected_object):
	table_info = {
		"Name":			"artefacts",
		"Indexes":		{
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=50),
			
			database.Integer_field("team"),
			database.Integer_field("city"),
			
			database.Text_field("description"),
		),
		
		"Link tables":	(),
	}
	
	def __init__(self, row = {}):
		super(Artefact, self).__init__(row)
		
		#### Link tables
		# Artefact history, stores the location of each artefact each turn
		# tempLink = database.DB_link_object()
		# tempLink.table_name		= "artefact_history"
		# tempLink.primary_keys	= ["artefact", "turn"]
		# tempLink.indexes		= []
		# tempLink.add_field('artefact',	'int')
		# tempLink.add_field('team',		'int')
		# tempLink.add_field('turn',		'int')
		# self.link_tables.append(tempLink)

