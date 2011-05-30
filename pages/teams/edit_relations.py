import database
from pages import common
from queries import team_q
from classes import team

page_data = {
	"Admin":	True,
	"Redirect":	"View relations",
}

def main(cursor):
	t1 = team_q.get_one_team(cursor, int(common.get_val('t1')))
	t2 = team_q.get_one_team(cursor, int(common.get_val('t2')))
	
	relations = team_q.get_relations(cursor)
	
	output = []
	
	output.append("""
	<div style="padding:5px;">
	<span class="stitle"><strong>{t1} relation to {t2}</strong></span><br />
	<br />
	
	{t1} is {t12_border} towards {t2}<br />
	{t2} is {t21_border} towards {t1}<br />
	<br />
	
	{t1} has a tax rate of {t12_tax}% towards {t2}<br />
	{t2} has a tax rate of {t21_tax}% towards {t1}<br />
	<br />
	
	</div>
	""".format(
		t1 = t1.name,
		t2 = t2.name,
		
		t12_border = team.border_states[relations.get(t1.id, {}).get(t2.id, {}).get('border', t1.default_borders)],
		t21_border = team.border_states[relations.get(t2.id, {}).get(t1.id, {}).get('border', t2.default_borders)],
		
		t12_tax = relations.get(t1.id, {}).get(t2.id, {}).get('taxes', t1.default_taxes),
		t21_tax = relations.get(t2.id, {}).get(t1.id, {}).get('taxes', t2.default_taxes),
	))
	
	output.append("</div>")
	
	return "".join(output)