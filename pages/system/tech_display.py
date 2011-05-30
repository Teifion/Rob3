import database
from pages import common
from data_classes import tech
from queries import tech_q
from classes import res_dict

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	tech_dict = tech_q.get_all_techs(cursor)
	
	output	= []
	count	= 0
	for tech_id, the_tech in tech_dict.items():
		if the_tech.name == "NONE": continue
		
		base_cost	= res_dict.Res_dict(the_tech.base_cost)
		extra_cost	= res_dict.Res_dict(the_tech.extra_cost)
	
		materials	= "%s + L x %s" % (base_cost.get("Materials"), extra_cost.get("Materials"))
		points		= "%s + L x %s" % (base_cost.get("Tech points"), extra_cost.get("Tech points"))
	
		count += 1
	
		output.append("""
		<tr class='row%(count)s'>
			<td><a id='%(js_name)s' href='#%(js_name)s'>%(name)s</a></td>
			<td>%(materials)s</td>
			<td>%(points)s</td>
			<td>%(description)s</td>
			<td><input type='text' id='lvl%(js_name)s' onkeyup="var lvl = $('#lvl%(js_name)s').val();
			$('#mat%(js_name)s').html(%(materials_base)s + (lvl * %(materials_extra)s));
			$('#pts%(js_name)s').html(%(points_base)s + (lvl * %(points_extra)s));" value='0' size='5'/></td>
			<td style='width: 50px;'>
				<span id='mat%(js_name)s'>0</span>, 
				<span id='pts%(js_name)s'>0</span>
			</td>
		</tr>""" % {
			"count":			count%2,
			"name":		the_tech.name,
			"js_name":			common.js_name(the_tech.name).replace(" ", ""),
		
			"materials":		materials,
			"points":			points,
		
			"materials_base":	base_cost.get("Materials"),
			"materials_extra":	extra_cost.get("Materials"),
		
			"points_base":		base_cost.get("Tech points"),
			"points_extra":		extra_cost.get("Tech points"),
		
			"description":	the_tech.description,
		})

	return "".join(output)
