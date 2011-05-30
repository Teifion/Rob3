import time

def add_turn_timestamp(turn, timestamp=-1):
	if timestamp < 1:
		timestamp = int(time.time())
	
	query = "INSERT INTO turns (turn, turn_time) values (%s, %s);" % (turn, timestamp)
	return query

def delete_turn_timestamp(turn):
	return """DELETE FROM turns WHERE turn = %d;""" % turn

def get_warn_count(cursor):
	return len(get_warn_list(cursor))

def get_warn_list(cursor):
	output = []
	
	# Interactive orders
	query = """SELECT id, title FROM interactive_orders WHERE handled = False;"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		output.append(("interactive_order", row))
	
	return output