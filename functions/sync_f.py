import database
import re

foreign_key_re = re.compile(r'FOREIGN KEY \((.*?)\) REFERENCES (.*?)\((.*?)\)')
negative_default = re.compile(r'\((-[0-9]*)\)')

def check_table(cursor, table_info, fix=False, show_fixes=False, die_queitly=False):
	"""A wrapper for the check table function, simpy so we can have some decent exception handling"""
	
	# Run some checks
	has_pk = False
	for f in table_info['Fields']:
		if f.primary_key:
			has_pk = True
		
	if not has_pk:
		return database.shell_text("''%s'' has [r]no primary key[/r]" % table_info['Name'])
	
	# Now to actually build it
	try:
		return check_table_func(cursor, table_info, fix=fix, show_fixes=show_fixes)
	except Exception as e:
		if die_queitly:
			return database.shell_text("ERROR: Was not able to create [r]%s[/r]" % table_info['Name'])
		else:
			print("Error on table: %s" % table_info['Name'])
			raise

def check_table_func(cursor, table_info, fix=False, show_fixes=False):
	"""Compares the table to the item, if fix is enabled then it changes things, if not then it just issues warnings"""
	surplus_columns = []
	missing_columns = []
	broken_columns	= []
	
	surplus_indexes = []
	missing_indexes = []
	
	surplus_foreign = []
	missing_foreign = []
	broken_foreign	= []
	
	fixes = []
	
	found_columns = []
	found_indexes = []
	found_foreign = []
	
	# Get the table OID
	query = "SELECT c.oid FROM pg_catalog.pg_class c WHERE c.relname = '{0}'".format(table_info['Name'])
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	table_oid = None
	for row in cursor:
		table_oid = row['oid']
	
	# Get columns
	query = "SELECT column_default, data_type, column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name = '%s'" % table_info['Name']
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Full list of fields
	# 	{'character_octet_length': 1073741824, 'table_schema': 'public', 'character_maximum_length': 50, 'ordinal_position': 1, 'udt_catalog': 'rob3', 'scope_catalog': None, 'collation_catalog': None, 'domain_schema': None, 'maximum_cardinality': None, 'identity_increment': None, 'is_self_referencing': 'NO', 'is_generated': 'NEVER', 'domain_name': None, 'is_updatable': 'YES', 'dtd_name': '1', 'identity_minimum': None, 'table_name': 'artefacts', 'collation_name': None, 'numeric_scale': None, 'domain_catalog': None, 'data_type': 'character varying', 'generation_expression': None, 'numeric_precision_radix': None, 'interval_precision': None, 'scope_name': None, 'collation_schema': None, 'column_default': "''::character varying", 'udt_name': 'varchar', 'numeric_precision': None, 'identity_cycle': None, 'identity_start': None, 'udt_schema': 'pg_catalog', 'character_set_name': None, 'scope_schema': None, 'interval_type': None, 'identity_generation': None, 'character_set_schema': None, 'is_nullable': 'NO', 'is_identity': 'NO', 'datetime_precision': None, 'character_set_catalog': None, 'table_catalog': 'rob3', 'column_name': 'name', 'identity_maximum': None}
	
	# List we may care about
	# 'character_maximum_length': 50,
	# 'data_type': 'character varying'
	# 'column_default': "''::character varying"
	# 'is_nullable': 'NO'
	# column_name': 'name'
	
	# No rows means the table is not there
	if cursor.rowcount == 0:
		if fix:
			o = create_table(cursor, table_info, show_fixes)
			return "\n".join([o, database.shell_text("%s created" % table_info['Name'])])
		else:
			if show_fixes:
				o = create_table(cursor, table_info, show_fixes)
				return "\n".join([o, database.shell_text("[r]Table missing[/r] (%s)" % table_info['Name'])])
			else:
				return database.shell_text("[r]Table missing[/r] (%s)" % table_info['Name'])
	
	# We're not remaking the table, lets check indexes
	field_list = [f.name for f in table_info['Fields']]
	
	for row in cursor:
		# Find out if this column should exist
		if row["column_name"] in field_list:
			found_columns.append(row["column_name"])
			
			# Now to make sure it's configured correctly
			f = table_info['Fields'][field_list.index(row["column_name"])]
			wrong_default = False
			wrong_type = False
			
			# Yes, we need both replaces, weird...
			if type(row['column_default']) == str:
				row['column_default'] = row['column_default'].replace("''::character varying", '')
				row['column_default'] = row['column_default'].replace("::character varying", '')
				row['column_default'] = row['column_default'].replace("''::text", '')
				row['column_default'] = negative_default.sub(r'\1', row['column_default'])
			
			# Now to check it is correct
			if f.field_type == "Serial":
				wrong_default = False
			elif f.foreign_table != "" and f.foreign_col != "":
				wrong_default = False
			elif row['column_default'] == None:
				wrong_default = True
			elif f.field_type == "integer":
				if str(row['column_default']) != str(f.default):
					wrong_default = True
			elif f.field_type == "double precision":
				if float(row['column_default']) != float(f.default):
					wrong_default = True
			elif f.field_type == "boolean":
				if (row['column_default'] == "false" and f.default == True) or \
					(row['column_default'] == "true" and f.default == False):
					wrong_default = True
			elif row['column_default'] != f.default:
				wrong_default = True
			
			if row['data_type'] != f.desc_name: wrong_type = True
			
			if wrong_default or wrong_type:
				broken_columns.append(f.name)
				
				# Default needs to be fixed for strings
				if f.field_type in ("text", "Varchar"):
					correct_default = "'%s'" % database.escape(f.default)
				else:
					correct_default = f.default
				
				if wrong_default:
					print("%s: Wanted Default: %s, DB Default: %s" % (f.name, correct_default, row['column_default']))
					
					if wrong_type:
						print("%s: Wanted Type - %s, DB Type: %s" % (f.name, f.desc_name, row['data_type']))
						# raise Exception("No fix for this yet")
						fixes.append("ALTER TABLE {0} ALTER COLUMN {1} TYPE {2}".format(table_info['Name'], f.name, f.data_type_syntax()))
						fixes.append("ALTER TABLE {0} ALTER COLUMN {1} SET DEFAULT {2};".format(table_info['Name'], f.name, correct_default))
						
					else:
						fixes.append("ALTER TABLE {0} ALTER COLUMN {1} SET DEFAULT {2};".format(table_info['Name'], f.name, correct_default))
				else:
					fixes.append("ALTER TABLE {0} ALTER COLUMN {1} TYPE {2}".format(table_info['Name'], f.name, f.data_type_syntax()))
		else:
			surplus_columns.append(row['column_name'])
			fixes.append("alter table %s drop %s" % (table_info['Name'], row["column_name"]))
	
	# Any leftover properties?
	for f in table_info["Fields"]:
		if f.name not in found_columns:
			missing_columns.append(f.name)
			fixes.append("alter table %s add column %s" % (table_info['Name'], f.create_column()))
	
	# Any indexes? - Query comes from PhpPgAdmin
	query = """SELECT c2.relname AS indname, i.indisprimary, i.indisunique, pg_get_indexdef(i.indexrelid) AS inddef,
				obj_description(c.oid, 'pg_index') AS idxcomment
			FROM pg_class c, pg_class c2, pg_index i
			WHERE c.relname = '%s' AND c.oid = i.indrelid AND i.indexrelid = c2.oid""" % table_info['Name']
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		if row["indisprimary"] == True: continue
		
		real_index_name = row["indname"].replace('%s_index_' % table_info['Name'], '')
		
		if real_index_name in table_info['Indexes']:
			found_indexes.append(real_index_name)
		else:
			surplus_indexes.append(real_index_name)
			fixes.append("drop index %s;" % (row["indname"]))
	
	# Any leftover indexes?
	for i_name, i_content in table_info['Indexes'].items():
		if not (i_name in found_indexes):			
			missing_indexes.append(i_name)
			fixes.append("create index %s_index_%s on %s (%s);" % (table_info['Name'], i_name, table_info['Name'], i_content))
	
	# Foreign keys?
	query = """SELECT conname, pg_catalog.pg_get_constraintdef(r.oid, true) as condef
	FROM pg_catalog.pg_constraint r
	WHERE r.conrelid = '{0}' AND r.contype = 'f'""".format(table_oid)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		x = foreign_key_re.search(row["condef"])
		if x != None:
			found = False
			for f in table_info["Fields"]:
				if f.name == x.groups()[0]:
					found = True
					
					if f.foreign_table == "" and f.foreign_col == "":
						surplus_foreign.append(f.name)
						fixes.append("ALTER TABLE {0} DROP CONSTRAINT {1};".format(table_info['Name'], row['conname']))
					
					elif f.foreign_table != x.groups()[1] or f.foreign_col != x.groups()[2]:
						# Wrong foreign
						broken_foreign.append(f.name)
						raise Exception("No fix created")
						# fixes.append("ALTER TABLE {0} ADD CONSTRAINT fk{1} FOREIGN KEY ({1}) REFERENCES {2} ({3});".format(table_info['Name'], f.name, f.foreign_table, f.foreign_col))
					else:
						found_foreign.append(f.name)
			
			if not found:
				missing_foreign.append(f.name)
				raise Exception("No fix created")
	
	for f in table_info["Fields"]:
		if f.foreign_table != "" or f.foreign_col != "":
			if f.name not in found_foreign:
				missing_foreign.append(f.name)
				fixes.append("ALTER TABLE {0} ADD CONSTRAINT fk{1} FOREIGN KEY ({1}) REFERENCES {2} ({3});".format(table_info['Name'], f.name, f.foreign_table, f.foreign_col))
	
	# Are we green?
	if len(fixes) == 0:
		return database.shell_text("[g]%s is correct[/g]" % table_info['Name'])
	else:
		output = []
		
		# Columns
		if fix:
			for f in fixes:
				try:
					cursor.execute(f)
				except Exception as e:
					if "REFERENCES" in f:
						print(f)
						raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
						pass
					else:
						print("ERROR")
						print(fixes)
						print("")
						print(f)
						print("")
						raise
			
			if show_fixes:
				print("\n".join(fixes))
				
			output.append(database.shell_text("%s fixed" % table_info['Name']))
			return "\n".join(output)
			
		else:
			for c in surplus_columns:
				output.append(database.shell_text("[r]column surplus in %s[/r] (%s)" % (table_info['Name'], c)))
		
			for c in missing_columns:
				output.append(database.shell_text("[r]column missing in %s[/r] (%s)" % (table_info['Name'], c)))
			
			for c in broken_columns:
				output.append(database.shell_text("[r]column broken in %s[/r] (%s)" % (table_info['Name'], c)))
			
			# Indexes
			for i in surplus_indexes:
				output.append(database.shell_text("[r]index surplus in %s[/r] (%s)" % (table_info['Name'], i)))
			
			for i in missing_indexes:
				output.append(database.shell_text("[r]index missing in %s[/r] (%s)" % (table_info['Name'], i)))
			
			# Foreign keys
			for f in broken_foreign:
				output.append(database.shell_text("[r]bad foreign in %s[/r] (%s)" % (table_info['Name'], f)))
			
			for f in missing_foreign:
				output.append(database.shell_text("[r]missing foreign for %s[/r] (%s)" % (table_info['Name'], f)))
				
			for f in surplus_foreign:
				output.append(database.shell_text("[r]surplus foreign in %s[/r] (%s)" % (table_info['Name'], f)))
			
			if show_fixes:
				output.append("  Fixes:")
				
				for f in fixes:
					output.append(f)
			
				output.append("")
			
			return "\n".join(output)
	
	return database.shell_text("[g]%s is correct[/g]" % table_info['Name'])
	
	# if fix:
	# 	result = database.check_table(my_item, 1)
	# 	if result == 'fixed':
	# 		database.check_table(my_item)
	# else:
	# 	database.check_table(my_item)
	# 
	# check_link_table(my_item, fix)


# These functions are used by the Database checker program to create/edit the tables
def create_table(cursor, table_info, show_fixes=False):
	"""Creates a table from the item"""
	query = "drop table %s;" % table_info['Name']
	try:					cursor.execute(query)
	except Exception as e:	pass
	
	query = ["create table %s" % table_info['Name']]
	query.append("(")
	
	# for prop, prop_type in my_item.property_dict.items():
	pks = []
	for f in table_info['Fields']:
		if f.primary_key: pks.append(f.name)
		
		query.append(f.create_field())
	
	query.append("primary key (%s)" % (",".join(pks)))
	query.append(")")
	
	# Bring it all together
	query = "\n".join(query)
	
	# print(query)
	# exit()
	
	if show_fixes:
		output = [query]
	else:
		try:	 cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
		output = [database.shell_text('%s created [g]successfully[/g]' % table_info['Name'])]
	
	
	# Any indexes? - Query comes from PhpPgAdmin
	index_queries = []
	found_indexes = []
	missing_indexes = []
	surplus_indexes = []
	
	query = """SELECT c2.relname AS indname, i.indisprimary, i.indisunique, pg_get_indexdef(i.indexrelid) AS inddef,
				obj_description(c.oid, 'pg_index') AS idxcomment
			FROM pg_class c, pg_class c2, pg_index i
			WHERE c.relname = '%s' AND c.oid = i.indrelid AND i.indexrelid = c2.oid""" % table_info['Name']
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		if row["indisprimary"] == True: continue
		
		real_index_name = row["indname"].replace('%s_index_' % table_info['Name'], '')
		
		if real_index_name in table_info['Indexes']:
			found_indexes.append(real_index_name)
		else:
			surplus_indexes.append(real_index_name)
			index_queries.append("drop index %s;" % (row["indname"]))
	
	# Any leftover indexes?
	for i_name, i_content in table_info['Indexes'].items():
		if not (i_name in found_indexes):			
			missing_indexes.append(i_name)
			index_queries.append("create index %s_index_%s on %s (%s);" % (table_info['Name'], i_name, table_info['Name'], i_content))
	
	for query in index_queries:
		if show_fixes:
			output.append(query)
		else:
			try: cursor.execute(query)
			except Exception as e:
				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
			output.append(database.shell_text('index_%s added to %s [g]successfully[/g]' % (i_name, table_info['Name'])))
	
	return "\n".join(output)

def fill_table(cursor, table_info, data_module):
	"""Fills a list table"""
	inserts		= []
	field_names	= []
	
	# Make the table
	query = "DROP TABLE %s" % table_info['Name']
	try: cursor.execute(query)
	except Exception as e:
		pass
	# return ""
	create_table(cursor, table_info)
	
	# Field names
	field_names = [f.name for f in table_info['Fields']]
	
	# Rows
	for i, block in enumerate(data_module.data_list):
		values = []
		for f in table_info['Fields']:
			if f.name == "id":
				current_val = i
			else:
				current_val = getattr(block, f.name)
			
			if current_val.__class__ == float:
				if current_val == int(current_val):
					current_val = int(current_val)
			
			if current_val.__class__ == str:
				current_val = "%s" % database.escape(current_val)
			
			values.append("'%s'" % current_val)
		
		inserts.append("(%s)" % ",".join(values))
	
	query = "INSERT INTO %s (%s) values %s;" % (table_info['Name'], ",".join(field_names), ",".join(inserts))
	try:
		cursor.execute(query)
		return database.shell_text("[y]Filled %s[/y] with %s rows" % (table_info['Name'], len(inserts)))
	except Exception as e:
		print("Query: %s\n" % query)
		raise e
		
