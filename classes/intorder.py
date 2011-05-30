import database
import re
from classes import order_post

patterns = {
	"rob_box":		re.compile(r'(?i)\[rob\](?P<content>.*?)\[/rob\]'),
	"targets":		re.compile(r'(?i)\[b\]Targets:\[/b\](?P<targets>.*?)(?:\n|$)'),
	"cities":		re.compile(r'(?i)\[b\]Cities:\[/b\](?P<cities>.*?)(?:\n|$)'),
	"departure":	re.compile(r'(?i)\[b\]Departure:\[/b\](?P<departure>.*?)(?:\n|$)'),
	"allies":		re.compile(r'(?i)\[b\]Allies:\[/b\](?P<allies>.*?)(?:\n|$)'),
	"forces":		re.compile(r'(?i)\[b\]Forces:\[/b\](?P<forces>.*?)(?:\n|$)'),
}


class Intorder (database.DB_connected_object):
	table_info = {
		"Name":			"intorders",
		"Indexes":		{
			# "team":	"team",
		},
		"Fields":		(
			database.Integer_field("id",	primary_key=True),
		),
	}
	
	def __init__(self, row = {}, parent=None):
		super(Intorder, self).__init__(row)
		
		self.parent = parent
		self.sections = None
	
	def get_parent(self, cursor):
		cursor = database.get_cursor()
		query = """SELECT * FROM orders WHERE post_id = %d""" % self.id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		row = cursor.fetchone()
		self.parent = order_post.Order_post(the_world=None, row=row)
	
	def split(self, force_requery=False):
		if self.parent.content == "Orders placeholder":
			self.sections = []
			return self.sections
		
		if self.sections != None and not force_requery:
			return self.sections
		
		self.sections = []
		
		
		new_section = Int_section()
		new_section.content = self.parent.content
		
		self.sections.append(new_section)
		
		
		return self.sections

class Int_section (object):
	"""docstring for Int_section"""
	def __init__(self):
		super(Int_section, self).__init__()
		self.content = ""
		
		self.targets_str = ""
		self.cities_str = ""
		self.departure_str = ""
		self.allies_str = ""
		self.forces_str = ""
		
		self.cities_str = ""
	
	def de_string(self):
		"""Takes the items out of their string form and into pure variables"""
		
		"""
		[o]My order[/o]
		[rob][b]Target:[/b] Aracnar
		[b]Cities:[/b] Ansbach, Hildfriede, Greifwald
		[b]Departure:[/b] early January
		[b]Allies:[/b] Aracnar, Daninia, Holy Empire of Machtburg
		[b]Forces:[/b] Albed 3rd force, Albed 5th force, Albed 4th force
		[/rob]
		"""
		pass
	
	