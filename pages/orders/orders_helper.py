from pages import common
# from functions import oh_f
from classes import oh

page_data = {
	"Admin":	True,
	"Title":	"Orders helper",
	# "Headers":	True,
}

def main(cursor):
	team_id		= int(common.get_val('team', 0))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>%s" % (common.select_team_form(
			cursor, 'orders_helper', dev_mode=1, ajax=1
		), common.onload("$('#select_team_input').focus();"))
	
	the_oh = oh.Oh(cursor)
	the_oh.local_path = True
	the_oh.setup(true_team_list=[team_id])
	
	return the_oh.make_oh(team_id)