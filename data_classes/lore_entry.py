import database

levels = (
	"public",# Anybody can see it
	"secret",# You need to work to find it
	"gm",# Notes etc that only the GM can see
)

class Lore_entry (database.DB_connected_object):
	table_info = {
		"Name":			"lore_entries",
		"Indexes":		{
			"cat":	"cat",
			"page":	"page",
		},
		"Fields":		(
			database.Serial_field("id"),
			database.Varchar_field("cat",		max_length=40, primary_key=True),
			database.Varchar_field("page",		max_length=40, primary_key=True),
		),
	}
	
	def __init__(self, row = {}):
		super(Lore_entry, self).__init__(row)
		self.blocks = []
	
	def get_blocks(self, cursor):
		self.blocks = []
		
		query = """SELECT * FROM lore_blocks WHERE entry = %d ORDER BY id""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.blocks.append(row)
		
		return self.blocks
	
	def filter(self, cursor, level, filter_list):
		output = []
		for b in self.blocks:
			if b['level'] <= level:
				if filter_list == [] or b['name'] in filter_list:
					output.append(b)
		
		return output
			

Lore_block = {
	"Name":			"lore_blocks",
	"Indexes":		{
	},
	"Fields":		(
		database.Serial_field("id",			primary_key=True),
		database.Integer_field("entry"),#		foreign_key=("lore_entries", "id")),
		
		database.Integer_field("level"),
		database.Boolean_field("no_break"),
		database.Varchar_field("name",		max_length=40),
		database.Varchar_field("title",		max_length=40),
		database.Text_field("description"),
	),
}