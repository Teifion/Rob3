import database

# These functions are used by the Database checker program to create/edit the tables
def create_table(my_item):
	"""Creates a table from the item"""
	query = "drop table %s;" % my_item.table_name
	try:					cursor.execute(query)
	except Exception as e:	pass
	
	codeParts = ["create table %s" % my_item.table_name]
	codeParts.append("(")
	
	for prop, prop_type in my_item.property_dict.items():
		if prop in my_item.increment_fields:
			codeParts.append(create_field(prop, prop_type, ',', 1))
		else:
			codeParts.append(create_field(prop, prop_type, ','))
	
	codeParts.append("primary key (%s)" % (",".join(my_item.primary_keys)))
	codeParts.append(")")
	
	# Bring it all together
	query = "\n".join(codeParts)
	
	try:	 cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	print(shell_text('%s created [g]successfully[/g]' % my_item.table_name))
	
	for i in my_item.indexes:
		cursor.execute("create index index_%s on %s (%s)" % (i, my_item.table_name, i))
		print(shell_text('index_%s added to %s [g]successfully[/g]' % (i, my_item.table_name)))

def check_table(my_item, fix = 0):
	"""Compares the table to the item, if fix is enabled then it changes things, if not then it just issues warnings"""
	surplus_columns = []
	missingColumns = []
	
	surplusIndexes = []
	missingIndexes = []
	
	fixes = []
	
	foundColumns = []
	foundIndexes = []
	
	query_exception = False
	
	query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name = '%s'" % my_item.table_name
	try:
		cursor.execute(query)
		if cursor.rowcount == 0:
			query_exception = True
	except Exception:
		query_exception = True
	
	if query_exception:
		if fix == 1:
			create_table(my_item)
			print(shell_text("%s created" % my_item.table_name))
			return 'fixed'
		else:
			print(shell_text("[r]Table missing[/r] (%s)" % my_item.table_name))
			return 'broken'
	
	# We're not remaking the table, lets check indexes
	for row in cursor:
		# Find out if this field should exist
		if row["column_name"] in my_item.property_dict.keys():
			foundColumns.append(row["column_name"])
		else:
			surplus_columns.append(row['column_name'])
			fixes.append("alter table %s drop %s" % (my_item.table_name, row["column_name"]))
	
	# Any leftover properties?
	for k, v in my_item.property_dict.items():
		if not (k in foundColumns):
			missingColumns.append(k)
			fixes.append("ALTER TABLE %s ADD COLUMN %s" % (my_item.table_name, create_field(k, v)))
	
	
	# Any indexes? - Query comes from PhpPgAdmin
	query = """SELECT c2.relname AS indname, i.indisprimary, i.indisunique, pg_get_indexdef(i.indexrelid) AS inddef,
				obj_description(c.oid, 'pg_index') AS idxcomment
			FROM pg_class c, pg_class c2, pg_index i
			WHERE c.relname = '%s' AND c.oid = i.indrelid AND i.indexrelid = c2.oid""" % my_item.table_name
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		if row["indisprimary"] == True: continue
		
		real_index_name = row["indname"].replace('%s_index_' % my_item.table_name, '')
		
		if real_index_name in my_item.indexes:
			foundIndexes.append(real_index_name)
		else:
			surplusIndexes.append(real_index_name)
			fixes.append("drop index %s;" % (row["indname"]))
	
	# Any leftover indexes?
	for i in my_item.indexes:
		if not (i in foundIndexes):			
			missingIndexes.append(i)
			fixes.append("create index %s_index_%s on %s (%s);" % (my_item.table_name, i, my_item.table_name, i))
	
	
	# Are we green?
	if len(fixes) == 0:
		print(shell_text("[g]%s is correct[/g]" % my_item.table_name))
		return 'good'
	else:
		# Columns
		if fix == 1:
			for f in fixes:
				try:
					cursor.execute(f)
				except Exception as e:
					print(fixes)
					print("")
					print(f)
					print("")
					raise
			
			print(shell_text("%s fixed" % my_item.table_name))
			return 'fixed'
			
		else:
			for c in surplus_columns:
				print(shell_text("[r]column surplus in %s[/r] (%s)" % (my_item.table_name, c)))
		
			for c in missingColumns:
				print(shell_text("[r]column missing in %s[/r] (%s)" % (my_item.table_name, c)))
		
			# Indexes
			for i in surplusIndexes:
				print(shell_text("[r]index surplus in %s[/r] (%s)" % (my_item.table_name, i)))

			for i in missingIndexes:
				print(shell_text("[r]index missing in %s[/r] (%s)" % (my_item.table_name, i)))
		
			return 'broken'

def fill_table(table_name, data_array):
	"""Fills a list table"""
	
	inserts		= []
	field_names	= []
	
	# A list of column names
	for block in data_array:
		if block == "": continue
		for prop in block.properties:
			field_names.append(prop)
		
		break
	
	# Actual rows
	for block in data_array:
		if block == "": continue
		
		values = []
		for prop in field_names:
			current_val = getattr(block, prop)
			if current_val.__class__ == float:
				if current_val == int(current_val):
					current_val = int(current_val)
			
			if current_val.__class__ == str:
				current_val = "%s" % escape(current_val)
			
			values.append("'%s'" % current_val)
		
		inserts.append("(%s)" % ",".join(values))
	
	query = "INSERT INTO %s (%s) values %s;" % (table_name, ",".join(field_names), ",".join(inserts))
	try:
		cursor.execute(query)
		print(shell_text("[y]Filled %s[/y] with %s rows" % (table_name, len(inserts))))
	except Exception as e:
		print("Query: %s\n" % query)
		raise e
		

def create_field(field_name, field_type, append = '', auto_increment = 0):
	"""Used to create table fields based on a field type"""
	
	result = ""#int unsigned not null default 0,
	
	if field_type[0:6] == 'serial':
		result = "%s serial" % (field_name)
	
	if field_type[0:4] == 'char' or field_type[0:7] == 'varchar':
		size = re.search(r'\(([0-9]{1,3})\)', field_type)
		result = "%s varchar%s not null default ''" % (field_name, size.group(0))
	
	if field_type[0:4] == 'text' or field_type[0:4] == 'blob':
		result = "%s text not null default ''" % (field_name)
	
	if field_type[0:3] == 'int' or field_type[0:7] == 'integer':
		result = "%s int" % field_name
		
		if auto_increment == 1:	result += " not null auto_increment"
		else:					result += " not null default 0"
	
	if field_type[0:6] == 'double':
		result = "%s double precision" % field_name
		
		if auto_increment == 1:	result += " not null auto_increment"
		else:					result += " not null default 0"
	
	if field_type[0:4] == 'bool': result = "%s boolean not null default False" % field_name
	
	if result == "":
		exit("No type for '%s'" % field_type)
	
	return "%s%s" % (result, append)
