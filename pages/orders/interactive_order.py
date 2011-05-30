from lore import pages
from pages import common
from functions import team_f
from queries import intorder_q
from classes import world


page_data = {
	"Title":	"Interactive order",
	"Admin":	True,
}

def main(cursor):
	order_id = int(common.get_val("order", -1))
	
	if order_id < 1:
		return "<div style='padding: 5px;'>%s</div>" %  "No order selected"
	
	the_order = intorder_q.get_interactive(cursor, order_id)
	the_order.the_world = world.World(cursor)
	the_order.interactive_setup(cursor)
	
	# Points to make
	points_template = "<label for='pt_{i}'>{p}</label>: <input type='checkbox' id='pt_{i}' value='1' />"
	
	points_template = """
	<tr id="row_{i}" class="">
		<td><label for="pt_{i}" style="width:100%; display:block;">{p}</label></td>
		<td style="padding:2px;"><input type="checkbox" name="pt_{i}" id="pt_{i}" value="True" onchange="if ($('#pt_{i}').attr('checked')) {{$('#row_{i}').addClass('selected_army');}} else {{$('#row_{i}').removeClass('selected_army');}} calc_amount();"/></td>
		<td>&nbsp;</td>
	</tr>
	"""
	
	output = []
	output.append('<div style="padding:10px;">')
	
	# Get to work
	output.append("""
	<div style="border: 1px solid #000;">
		{pre_calculations}
	</div>
	<div style="width: 40%; float:left; border: 1px solid #000;">
		{content}
	</div>
	<div style="width: 30%; float:left; border: 1px solid #000;">
	<table border="0" cellspacing="0" cellpadding="5">
		{points}
	</table>
		<!--{points}-->
	</div>
	<div style="border: 1px solid #000; clear: left;">
		{post_calculations}
		Score: <span id="score">0</span>
		<br /><br />
		
		<form action="web.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="direct_query" />
			<textarea name="query" id="query" rows="4" style="font-family:monospace; width: 60%;">-- No queries at present</textarea>
			
			<input type="submit" value="Run query" />
		</form>
		<textarea name="result" id="result" rows="4" style="font-family:monospace; width: 60%;">[o]{title}[/o]\nNo results</textarea>
	</div>
	""".format(
		content	= the_order.interactivity['content'],
		points	= "".join([points_template.format(i=i, p=p) for i, p in enumerate(the_order.interactivity['points'])]),
		pre_calculations = the_order.interactivity['pre_calculations'],
		post_calculations = "",
		title = the_order.title_name,
	))
	
	js_points = "if ($('#pt_%(i)d').attr('checked') == true) {points++;}"
	
	page_data['javascript'] = """
	function calc_amount ()
	{
		multiplier = %(multiplier)d;
		points = 0;
		%(check_points)s
		
		score = ((points*multiplier)/%(max_score)d)*100;
		
		$('#score').html(Math.round(score) + "%%, Muliplier: %(multiplier)s");
		$('#query').html(query_func(score) + "\\nUPDATE interactive_orders SET handled = True WHERE id = %(order_id)d;");
		$('#result').html(result_func(score));
	}
	function query_func (score)
	{
		%(query_func)s
	}
	function result_func (score)
	{
		%(result_func)s
	}
	""" % {
		"order_id":	order_id,
		"check_points":	"\n".join([js_points % {"i":i} for i, p in enumerate(the_order.interactivity['points'])]),
		"multiplier": the_order.interactivity['multiplier'],
		"max_score": len(the_order.interactivity['points']),
		"query_func": the_order.interactivity['query_func'],
		"result_func": the_order.interactivity['result_func'],
		"multiplier": the_order.interactivity['multiplier'],
	}
	
	output.append('</div>%s' % common.onload('calc_amount();'))
	
	return "".join(output)