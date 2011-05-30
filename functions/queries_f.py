import time
import database
from pages import common
from classes import queries

def log_query(cursor, query_data, subject="No subject"):
	query = """INSERT INTO queries (query_data, time, turn, subject)
		values
		('%(data)s', %(time)s, %(turn)s, %(subject)s);""" % {
			"data":		database.escape(query_data),
			"time":		int(time.time()),
			"turn":		common.current_turn(),
			"subject":	queries.subjects.index(subject),
		}
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))