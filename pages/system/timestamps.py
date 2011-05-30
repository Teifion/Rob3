import database
import time
import urllib.request
from pages import common
from functions import system_f
from queries import system_q

page_data = {
	"Title":	"Turn timestamps",
	"Admin":	True,
}

def main(cursor):
	post_id 			= int(common.get_val('post', 0))
	turn				= int(common.get_val('turn', 0))
	timestamp			= int(common.get_val('timestamp', 0))
	
	delete_timestamp	= int(common.get_val('delete_timestamp', 0))
	
	output = ['<div style="padding: 5px;">']
	
	if post_id > 0 and turn > 0:
		getter_data = "p=%s&mode=postTime&post=%d" % (common.data['getterPass'], post_id)
		timestamp = int(urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip())
		
		database.query(cursor,
			system_f.add_turn_timestamp(turn, timestamp))
		
		output.append('Post %d was posted at %s<br /><br />' % (post_id, timestamp))
	
	elif timestamp > 0 and turn > 0:
		database.query(cursor,
			system_f.add_turn_timestamp(turn, timestamp))
	
	# Deletion
	if delete_timestamp > 0:
		database.query(cursor,
			system_f.delete_turn_timestamp(delete_timestamp))
	
	current_turn = common.current_turn(force_requery=True)
	
	# Form to set timestamps
	output.append("""
	<form action="web.py" method="post" accept-charset="utf-8" style="width: 400px; float: left;">
		<input type="hidden" name="mode" value="timestamps" />
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="turn">Turn:</label></td>
				<td>%(turn)s</td>
			</tr>
			<tr>
				<td><label for="post">Post:</label></td>
				<td><input type="text" name="post" id="post" value="" size="15"/></td>
			</tr>
		</table>
	
		<input type="submit" value="Set turn timestamp" />
	</form>

	<form action="web.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="timestamps" />
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="turn_new">Turn:</label></td>
				<td><input type="text" name="turn" id="turn_new" value="%(last_turn)s" /></td>
			</tr>
			<tr>
				<td>Timestamp:</td>
				<td><input type="text" name="timestamp" id="timestamp" value="%(time_now)s" /></td>
			</tr>
		</table>
	
		<input type="submit" value="Set turn timestamp" />
	</form>
	<br /><br />
	""" % {
		"turn": common.text_box("turn", current_turn+2),
		"last_turn": current_turn+2,
		"time_now":	int(time.time()),
	})

	# Get turns
	output.append("""<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Turn</th>
			<th colspan="2">Time</th>
			<th>&nbsp;</th>
		</tr>""")

	turn_dict = system_q.most_recent_turns(cursor, limit=30)
	
	count = 1
	for t, turn_time in turn_dict.items():
		count += 1
		output.append("""
		<tr class="row%(row)s">
			<td>%(turn)s</td>
			<td>%(string)s</td>
			<td>%(epoch)s</td>
			<td style="padding:0px;"><a href="timestamps&amp;delete_timestamp=%(turn)s" class="block_link">Delete</a></td>
		</tr>""" % {
			"row":		(count%2),
			"turn":		t,
			"string":	time.strftime("%A, %d %B %Y", time.localtime(turn_time)),
			"epoch":	turn_time,
		})
	
	output.append("</table>")
	output.append("</div>")
	
	return "".join(output)