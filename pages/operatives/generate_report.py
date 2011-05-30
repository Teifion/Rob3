from pages import common
from functions import spy_report_f
from classes import spy_world

page_data = {
	"Title":	"Spy reports",
	"Admin":	True,
}

def main(cursor):
	output = ['<div style="padding:5px;">']
	
	# Get input
	team	= int(common.get_val("team", 0))
	city	= int(common.get_val("city", 0))
	target_team	= int(common.get_val("target_team", 0))
	area	= common.get_val("area", "")
	radius	= int(common.get_val("radius", 10))
	
	if city < 1 and target_team > 0:
		return team_main(cursor)
	
	the_world = spy_world.Spy_world(cursor)
	
	reports = spy_report_f.generate_report(the_world, team, city, area, radius)
	
	for r in reports:
		output.append('<div style="float: left; margin-right: 15px;">')
		output.append('<span class="stitle">%s</span><br />' % r.report_type)
		output.append('<textarea rows="8" cols="40">')
		output.append(r.content)
		output.append("</textarea></div>")
	
	output.append('</div>')
	return "".join(output)

def team_main(cursor):
	output = ['<div style="padding:5px;">TEAM']
	
	# Get input
	team		= int(common.get_val("team", 0))
	target_team	= int(common.get_val("target_team", 0))
	area		= common.get_val("area", "")
	radius		= int(common.get_val("radius", 10))
	
	the_world = spy_world.Spy_world(cursor)
	
	city_dict = the_world.cities_from_team(target_team)
	
	report_total = {}
	for city in city_dict.keys():
		reports = spy_report_f.generate_report(the_world, team, city, area, radius)
		
		for r in reports:
			if r.report_type not in report_total:
				report_total[r.report_type] = []
			
			report_total[r.report_type].append(r.content)
	
	for title, content in report_total.items():
		output.append('<div style="float: left; margin-right: 15px;">')
		output.append('<span class="stitle">%s</span><br />' % title)
		output.append('<textarea rows="8" cols="40">')
		output.append("\n".join(content))
		output.append("</textarea></div>")
	
	output.append('</div>')
	return "".join(output)