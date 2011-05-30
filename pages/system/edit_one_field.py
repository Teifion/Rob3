from pages import common
import database

page_data = {
	"Admin":	True,
	"Header":	False
}

def main(cursor):
	table_name		= common.get_val("table", "")
	field_name		= common.get_val("field", "")
	new_value		= common.get_val("value", "").strip()
	where			= common.get_val("where", "")
	
	new_value_db = new_value
	try:
		if new_value_db != float(new_value_db) and new_value_db != int(new_value_db):
			new_value_db = "'%s'" % database.escape(new_value_db)
	except Exception as e:
		new_value_db = "'%s'" % database.escape(new_value_db)
	
	query = """UPDATE %(table)s SET %(field)s = %(value)s WHERE %(where)s;""" % {
		"table":	table_name,
		"field":	field_name,
		"value":	new_value_db,
		"where":	where,
	}
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	return new_value