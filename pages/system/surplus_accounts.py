from pages import common
import urllib.request
from queries import player_q

page_data = {
	"Title":	"Surplus accounts",
	"Admin":	True,
}

def main(cursor):
	player_dict = player_q.get_all_players(cursor)
	
	getter_data = "p=%s&mode=surplus_accounts" % (common.data['getterPass'])
	surplus_list = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	surplus_list = surplus_list.decode('utf-8').split("\n")
	surplus_list = [int(s) for s in surplus_list]
	
	output = ["""<div style='padding:5px;'>
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Player</th>
			<th>Edit</th>
		</tr>
	"""]
	
	i = -1
	for s in surplus_list:
		if s not in player_dict: continue
		p = player_dict[s]
		
		if p.ir or p.not_surplus: continue
		
		i += 1
		
		# Equipment output
		output.append("""
		<tr class="row{r}">
			<td><a href="http://woarl.com/board/memberlist.php?mode=viewprofile&amp;u={id}">{name}</a></td>
			<td style="padding:0px;"><a href="web.py?mode=edit_player&amp;player={id}" class="block_link">Edit</a></td>
		</tr>
		""".format(
			r = i % 2,
			id = s,
			name = p.name,
		))
	
	output.append('</table></div>')
	
	return "".join(output)