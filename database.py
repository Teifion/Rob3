# And import stuff
import re
import bpgsql3 as bpgsql

host		= 'localhost'

username	= 'rob3'
password	= 'PASSWORD'
dbname		= 'rob3'

def query_batch(cursor, qlist, rollback=False):
	cursor.execute("BEGIN")
	for q in qlist:
		if q[0:2] == "--": continue
		try: cursor.execute(q)
		except Exception as e:
			cursor.execute("ROLLBACK")
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), q))
	
	if rollback:	cursor.execute("ROLLBACK")
	else:			cursor.execute("COMMIT")

def query_list(cursor, qlist):
	for q in qlist:
		if q[0:2] == "--": continue
		try: cursor.execute(q)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), q))

def query(cursor, *queries):
	for q in queries:
		if type(q) == list or type(q) == tuple:
			query_list(cursor, q)
		else:
			if q[0:2] == "--": continue
			try: cursor.execute(q)
			except Exception as e:
				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), q))

def get_custom_cursor(username, password, host, dbname, dictionaries=True):
	try:
		connection = bpgsql.connect(None, username, password, host, dbname)
	except Exception:
		raise
	
	return connection.cursor(dictionaries)
	
def get_cursor(dictionaries=True):
	return get_custom_cursor(username, password, host, dbname, dictionaries)

def get_test_cursor(dictionaries=True):
	return get_cursor(dictionaries)
	# return get_custom_cursor(t_username, t_password, t_host, t_dbname, dictionaries)

# Connect to the database
# cursor = get_cursor(True)


"""
Converts text to display in the shell with pretty colours

Bold:			''{TEXT}''
Underline:		__{TEXT}__
Blink:			**{TEXT}** <= Also makes it bold

Colour:			<colour>{TEXT}</colour> (with the pointed brackets)
Colours supported: Red, Green, Yellow, Blue, Magenta, Cyan
"""
shell_patterns = (
	(re.compile(r"''([^']*)''"), '\033[1;1m\\1\033[30;0m'),# Bold
	(re.compile(r'__([^_]*)__'), '\033[1;4m\\1\033[30;0m'),# Underline
	(re.compile(r"\*\*([^*]*)\*\*"), '\033[1;5m\\1\033[30;0m'),# Blink + Bold
	
	(re.compile(r"\[r\](.*?)\[\/r\]"),			'\033[31m\\1\033[30;0m'),# Red
	(re.compile(r"\[g\](.*?)\[\/g\]"),		'\033[32m\\1\033[30;0m'),# Green
	(re.compile(r"\[y\](.*?)\[\/y\]"),		'\033[33m\\1\033[30;0m'),# Yellow
	(re.compile(r"\[b\](.*?)\[\/b\]"),			'\033[34m\\1\033[30;0m'),# Blue
	(re.compile(r"\[m\](.*?)\[\/m\]"),	'\033[35m\\1\033[30;0m'),# Magenta
	(re.compile(r"\[c\](.*?)\[\/c\]"),			'\033[36m\\1\033[30;0m'),# Cyan
)

def shell_text(text):
	"""
	Converts text to display in the shell with pretty colours
	
	Bold:			''{TEXT}''
	Underline:		__{TEXT}__
	Blink:			**{TEXT}** <= Also makes it bold
	
	Colour:			<colour>{TEXT}</colour> (with the pointed brackets)
	Colours supported: Red, Green, Yellow, Blue, Magenta, Cyan
	"""
	if type(text) != str:
		return text
	
	for regex, replacement in shell_patterns:
		text = regex.sub(replacement, text)
	
	# text = text.replace("[t][/t]", '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
	return text

# A field used in a database
class DB_Field (object):
	"""docstring for DB_Field"""
	def __init__(self, name, field_type, max_length=None, default="", primary_key=False, foreign_key=(), desc_name=""):
		super(DB_Field, self).__init__()
		self.name		= name
		self.field_type	= field_type
		self.default	= default
		self.max_length = max_length
		self.primary_key = primary_key
		
		if desc_name == "":
			self.desc_name = self.field_type
		else:
			self.desc_name = desc_name
		
		if foreign_key != ():
			self.foreign_table	= foreign_key[0]
			self.foreign_col	= foreign_key[1]
		else:
			self.foreign_table 	= ""
			self.foreign_col	= ""
	
	def validate(self, value):
		return value
	
	def escape(self, value):
		return value
	
	def create_column(self):
		if self.default == None:
			default_str = ""
		elif type(self.default) == str:
			default_str = "default '%s'" % escape(self.default)
		else:
			default_str = "default %s" % self.default
		
		if self.foreign_col != "" and self.foreign_table != "":
			foreign_str = "REFERENCES {0} ({1})".format(self.foreign_table, self.foreign_col)
		else:
			foreign_str = ""
		return "{0} {1} NOT NULL {2} {3}".format(self.name, self.data_type_syntax(), default_str, foreign_str)
	
	def data_type_syntax(self):
		return self.field_type
	
	def create_field(self):
		return "%s," % self.create_column()
	
class Varchar_field (DB_Field):
	def __init__(self, name, default="", **kwargs):
		kwargs["default"]		= kwargs.get("default", "")
		kwargs["max_length"]	= kwargs.get("max_length", 255)
		kwargs["desc_name"]		= "character varying"
		super(Varchar_field, self).__init__(name, field_type="Varchar", **kwargs)
	
	def data_type_syntax(self):
		return "varchar(%d)" % self.max_length
	
	def escape(self, value):
		return value.replace("\\", "\\\\").replace("'", "''")

class Text_field (DB_Field):
	def __init__(self, name, default="", **kwargs):
		kwargs["default"]		= kwargs.get("default", default)
		super(Text_field, self).__init__(name, field_type="text", **kwargs)
	
	def escape(self, value):
		return value.replace("\\", "\\\\").replace("'", "''")

class Integer_field (DB_Field):
	def __init__(self, name, default=0, **kwargs):
		kwargs["default"] = kwargs.get("default", default)
		super(Integer_field, self).__init__(name, field_type="integer", **kwargs)
	
	def validate(self, value):
		if value == "":
			return 0
		return int(value)

class Double_field (DB_Field):
	def __init__(self, name, default=0, **kwargs):
		kwargs["default"] = kwargs.get("default", 0)
		# kwargs["desc_name"]	= "double precision"
		super(Double_field, self).__init__(name, field_type="double precision", **kwargs)

	def validate(self, value):
		return float(value)

class Serial_field (DB_Field):
	def __init__(self, name, **kwargs):
		kwargs["default"] 	= None
		kwargs["desc_name"]	= "integer"
		super(Serial_field, self).__init__(name, field_type="Serial", **kwargs)

	def validate(self, value):
		return int(value)

class Boolean_field (DB_Field):
	def __init__(self, name, default=0, **kwargs):
		kwargs["default"] = kwargs.get("default", False)
		super(Boolean_field, self).__init__(name, field_type="boolean", **kwargs)
	
	def validate(self, value):
		return (True if value else False)

# Things strongly linked to existing tables
class DB_link_object (object):
	"""This is used simply to create link tables between two classes where it's a many-one, one-many or many-many relationship"""
	def __init__(self):
		self.table_name			= ''
		self.property_dict		= {}
		self.property_list		= []
		self.primary_keys		= []
		self.indexes			= []
		self.increment_fields	= []
		self.foreign_keys		= []
	
	def add_field(self, field_name, field_type, fk_table=None, fk_field=None):
		self.property_dict[field_name] = field_type
		self.property_list.append(field_name)


# Used for lists of data which don't actually go into the DB any more
class DB_list_row (object):
	"""Each item holds data for a row to be put into a database, it's used for the data that's held in Python code and then dumped into the database via the CLI"""
	
	defaults = {}
	
	def __init__(self, **values):
		self.properties = []
		for k, v in self.defaults.items():
			if k not in self.properties: self.properties.append(k)
			setattr(self, k, v)
		
		for k, v in values.items():
			if k not in self.properties: self.properties.append(k)
			setattr(self, k, v)
	
	def set_value(self, name, value):
		"""Sets the value of a property"""
		if name not in self.properties: self.properties.append(name)
		setattr(self, name, value)
	
	def set_values(self, **values):
		"""Allows the setting of several values
		
		Use: set_values(a=1, b=2)"""
		for k, v in values.items():
			if k not in self.properties: self.properties.append(k)
			setattr(self, k, v)
	
	def set_many_values(self, dict_pairs):
		"""Sets several values via a dictionary, depreciated in favour of 'set_values'"""
		for k, v in dict_pairs.items():
			if k not in self.properties: self.properties.append(k)
			setattr(self, k, v)


# This one is our bread and butter DB class
class DB_connected_object (object):
	table_info = {
		"Name":			"",
		"Indexes":		(),
		"Fields":		(),
		"Link tables":	(),
	}
	
	"""Base class for most classes used in the system"""
	def __init__(self, row = {}, **values):
		for f in self.table_info['Fields']:
			
			# Get the value
			if f.name in row:		v = row[f.name]
			elif f.name in values:	v = values[f.name]
			else:
				if f.default != None:
					setattr(self, f.name, f.default)
				continue
			
			# Validate it
			v = f.validate(v)
			
			setattr(self, f.name, v)
	
	def get_from_form(self, form_list):
		"""Fill the class up from a form submission"""
		http_dict = {}
		for http_data in form_list:
			http_dict[http_data.name] = http_data.value
		
		self.get_from_dict(http_dict)
	
	def get_from_dict(self, form_dict):
		"""Fill up the class from a dictionary"""
		# First we need to set every field to None
		for f in self.table_info["Fields"]:
			if f.name in form_dict:
				setattr(self, f.name, form_dict[f.name])
			else:
				setattr(self, f.name, None)
	
	def update(self, cursor, test_mode = False):
		"""Updates the database, test mode returns the query that will be run rather than running it"""
		fields = []
		primary_keys = []
		for f in self.table_info["Fields"]:
			f_value = getattr(self, f.name)
			
			if f_value != None:
				f_value = f.validate(f_value)
			else:
				if f.field_type == "boolean":
					f_value = False
			
			if f.primary_key:# We don't want to update this, we'll be using it in the where part
				if f_value == None:
					raise Exception("Primary key '%s' missing for '%s'" % (f.name, self.table_info['Name']))
				
				primary_keys.append("%s = %s" % (f.name, f_value))
			
			else:
				if f_value != None:
					if f.field_type in ("Varchar", "text"):
						fields.append("%s = '%s'" % (f.name, escape(f_value)))
					else:
						fields.append("%s = %s" % (f.name, f_value))
		
		query = "UPDATE %s SET %s WHERE %s;" % (self.table_info['Name'], ",".join(fields), " AND ".join(primary_keys))
		
		if test_mode:
			return query
		else:
			try: cursor.execute(query)
			except Exception as e:
				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
def escape(text):
	"""Helps to defeat the vile forces of SQL-injection!"""
	return text.replace("\\", "\\\\").replace("'", "''")
