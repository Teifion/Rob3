# Runs all checks
from data import queries
from pages import common

query_dict_c = queries.get_query_dict_c()
query_by_turn = queries.get_query_by_turn()

for t in range(common.current_turn(), common.current_turn()-5, -1):
	if t not in query_by_turn: continue
	
	print """<table border="0" cellspacing="0" cellpadding="5" style="width:100%%;">
	<tr class="row2">
		<th>Turn %d</th>
		<th>Query</th>
	</tr>""" % t
	
	i = -1
	for q in query_by_turn[t]:
		i += 1
		the_query = query_dict_c[q]
		print """
		<tr class="row%(i)s">
			<td>%(subject)s</td>
			<td style="padding:1px;"><textarea rows="1" style="width:99%%;">%(query)s</textarea></td>
		</tr>
		
		""" % {
			"i":		i%2,
			"subject":	queries.subjects[the_query.subject],
			"query":	the_query.query_data,
		}
	
	print "</table>"