import database
import re
import urllib.request
from pages import common

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	query = "SELECT id FROM teams ORDER BY id DESC LIMIT 1;"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	row = cursor.fetchone()
	if row == None:
		start_at = 1
	else:
		start_at = row['id'] + 1
	
	getter_data = "p=%s&mode=teams&startat=%d" % (common.data['getterPass'], start_at)
	
	getter_results = str(urllib.request.urlopen(common.data['getter_url'], getter_data).read())
	
	count = int(re.search(r'count:([0-9]{1,5})', getter_results).group(1))
	
	if count < 1:
		return """No more teams to add. Started counting at %d<br />
		Rob getter URL: %s""" % (start_at, common.data['getter_url'])
	else:
		reMatches = re.findall(r'group_id:([0-9]{1,5}), group_name:([^\n\\]*)', getter_results)
		
		teams = []
		for teamMatch in reMatches:
			teams.append("(%s, '%s')" % (teamMatch[0], database.escape(teamMatch[1])))
		
		query = "INSERT INTO teams (id, name) values %s;" % ", ".join(teams)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		return "%s teams added successfully" % len(teams)
	
