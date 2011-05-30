import database
from pages import common
from data import queries_f

page_data = {
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	queries = common.get_val("queries", "")
	subject = common.get_val("subject", "No subject")
	
	if queries == "":
		e = Exception("POST:'queries' was empty")
		raise e
	
	queries_list = queries.split("\n")

	database.cursor.execute("BEGIN")
	
	for q in queries_list:
		if q == '': continue
		if q[0:2] == '--': continue
	
		try:
			database.cursor.execute(q)
		except Exception as e:
			database.cursor.execute('ROLLBACK')
			print("Query: %s\n" % q)
			raise e
	
	database.cursor.execute('COMMIT')
	
	queries_f.log_query(queries, subject)
	
	return "All queries run successfully"
	print ""