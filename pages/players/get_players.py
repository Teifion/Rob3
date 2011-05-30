import urllib.request
import re
import database
from pages import common

page_data = {
	"Title":	"Get players",
	"Admin":	True,
}

def main(cursor):
	query = "SELECT id FROM players ORDER BY id DESC LIMIT 1;"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	row = cursor.fetchone()
	if row == None:
		start_at = 1
	else:
		start_at = row['id'] + 1
	
	# Grab results
	getter_data = "p=%s&mode=players&startat=%d" % (common.data['getterPass'], start_at)
	
	getter_results = str(urllib.request.urlopen(common.data['getter_url'], getter_data).read())
	
	count = int(re.search(r'count:([0-9]{1,5})', getter_results).group(1))
	
	if count < 1:
		return """No more players to add. Started counting at %d<br />
		Rob getter URL: %s""" % (start_at, common.data['getter_url'])
	else:
		reMatches = re.findall(r'user_id:([0-9]{1,5}), username:([^\n\\]*)', getter_results)
		
		teams = []
		for teamMatch in reMatches:
			teams.append("(%s, '%s')" % (teamMatch[0], database.escape(teamMatch[1])))
		
		query = "INSERT INTO players (id, name) values %s;" % ", ".join(teams)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		return "%s players added successfully" % len(teams)
	