from pages import common

page_data = {
	"Title":	"Direct query",
	"Admin":	True,
}

# Query templates
templates = (
	"SELECT id, content, turn, tags FROM logs WHERE team = X ORDER BY turn DESC",
)

def main(cursor):
	one_query	= common.get_val('one', False)
	query		= common.get_val('query')
	
	if one_query:
		queries = [query]
	else:
		queries = query.split("\r")
	
	output = ["""
	<form action="web.py?mode=direct_query" method="post" accept-charset="utf-8">
		One query: <input type="checkbox" name="one" value="True" />
		<textarea name="query" id="query" rows="5" style="width:99%%;">%s</textarea>
		<br />
		<input type="submit" value="Run" style="float:right;margin-right: 40px;font-size:1.2em;"/>
		<br /><br />
	</form>
	""" % query]
	
	output.append(common.onload("$('#query').focus();"))
	
	if query != "":
		output.append("<hr /><div id='qrun' style='background-color:#FFC;padding:5px;'>Query run successfully.</div><br /><br />")
		
		first_row = True
		headers = []
		data = []
		
		id_list = []
		i = 0
		
		if len(queries) > 1:
			cursor.execute('BEGIN')
			for q in queries:
				q = q.strip()
				if q == '': continue
				if q[0:2] == '--': continue
			
				try:
					cursor.execute(q)
				except Exception as e:
					print("\nError with '%s'" % q)
					cursor.execute('ROLLBACK')
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), q))
		
			cursor.execute('COMMIT')
		else:
			try:
				cursor.execute(query)
			except Exception as e:
				print("\nError with '%s'" % query)
				cursor.execute('ROLLBACK')
				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
			
			totals = {}
			try:
				for row in cursor:
					if "id" in row:
						id_list.append(str(row['id']))

					if first_row:
						for k, v in row.items():
							totals[k] = 0
							headers.append("<th>%s</th>" % k)
				
					data.append("<tr class='row%d'>" % (i % 2))
					for k, v in row.items():
						data.append("<td>%s</td>" % v)
					
						if type(v) in (int, float):
							totals[k] += v
					data.append("</tr>")
				
					first_row = False
					i += 1
			
				output.append("""<div style='padding:5px;'>
				<table border="0" cellspacing="0" cellpadding="5">
					<tr class='row2'>
						{headers}
					</tr>
					{data}
				</table></div>
				""".format(
					headers="".join(headers),
					data="".join(data),
				))

				output.append('&nbsp;Id list: <input type="text" value="%s" style="width: 400px;"/>' % ", ".join(id_list))
			except Exception as e:
				output.append('No result set')
	
	output.append('<br /><br /><table border="0" cellspacing="0" cellpadding="5">')
	for t in templates:
		output.append(
			"""<tr>
				<td onclick="$('#query').text('%s');">%s</td>
			</tr>""" % (t, t)
		)
	output.append('</table>%s' % common.onload("$('#qrun').animate({backgroundColor:'white'}, 3000);"))
	
	return "".join(output)