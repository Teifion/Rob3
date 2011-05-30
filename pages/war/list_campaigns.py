from pages import common
from queries import campaign_q, team_q

page_data = {
	"Title":	"Campaign list",
	"Admin":	True,
}

def main(cursor, turn=-1):
	output = ["""<div style="padding: 5px;">"""]
	onload = []
	turn = int(common.get_val("turn", turn))
	
	if turn < 1:
		turn = common.current_turn()
	
	campaign_dict	= campaign_q.get_campaigns_from_turn(cursor, turn)
	team_dict		= team_q.get_all_teams(cursor)
	
	# Form to select a different turn
	output.append("""
	<!--
	<div style="float:right;border:1px solid #000; width: 60%%;" id="turn_info">
		&nbsp;
	</div>
	-->
	
	<form action="web.py" method="get" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="list_campaigns" />
		Turn: <input type="text" name="turn" value="%s" />
		&nbsp;&nbsp;&nbsp; <input type="submit" value="Show" />
	</form>
	%s
	<br /><br />""" % (
		turn,
		common.onload("$('#turn_info').load('web.py',{'mode':'turn_info','ajax':'True'});")))
	
	# Now the actual table
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Turn</th>
			<th>Name</th>
			<th>Sides</th>
			<th>&nbsp;</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = 1
	for campaign_id, the_campaign in campaign_dict.items():
		count += 1
		
		the_campaign.get_sides_basic(cursor)
		
		team_string = []
		for s in range(1, the_campaign.sides+1):
			teams_on_side = the_campaign.sides_basic[s]
			
			if teams_on_side == []:
				teams_on_side_str = "None"
			else:
				teams_on_side_str = ", ".join([team_dict[t].name for t in teams_on_side])
			
			team_string.append("""{s}: {teams}""".format(
				s=s,
				teams=teams_on_side_str,
			))
		
		team_string = "<br />".join(team_string)
		
		output.append("""
			<tr class="row{count}">
				<td>{turn}</td>
				<td><strong>{name}</strong></td>
				<td>{teams}</td>
				<td style="padding:0px;"><a href="web.py?mode=setup_campaign&amp;campaign={campaign_id}" class="block_link">Setup</a></td>
				<td style="padding:0px;"><a href="web.py?mode=list_battles&amp;campaign={campaign_id}" class="block_link">Battles</a></td>
			</tr>
			<!--
			<tr class="row0">
				<td colspan="5" id="camp_{campaign_id}" style="padding:0px;"></td>
			</tr>
			-->
		""".format(
			turn=turn,
			# count=1,
			count=count%2,
			name=the_campaign.name,
			teams=team_string,
			campaign_id=campaign_id,
		))
		
		
		# onload.append("$('#camp_%(id)d').load('web.py', {'mode':'list_battles', 'ajax':'True', 'campaign':'%(id)d'});" % {
		# 	"id": campaign_id,
		# })
	
	# New campaign
	count += 1
	output.append("""
	<!-- PY -->
	<tr class="row{count}">
		<form action="exec.py" id="add_campaign_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="add_campaign" />
		<td style="padding: 1px;"><input type="text" name="turn" value="{turn}" size="5"/></td>
		<td style="padding: 1px;"><input type="text" name="name" id="name" value="" /></td>
		<td style="padding: 1px;"><input type="text" name="sides" value="2" size="3"/></td>
		<td style="padding: 0px;" colspan="2">
			<!--
			<a class="block_link" href="#" onclick="$('#add_campaign_form').submit(); return false;">Add</a>
			-->
			<input type="submit" value="Add" />
		</td>
		</form>
		{onload}
	</tr>
	<!-- PYEND -->
	""".format(
		turn=turn,
		count=count%2,
		onload=common.onload("$('#name').focus();%s" % "".join(onload)),
	))
	
	output.append("</table></div>")
	
	return "".join(output)