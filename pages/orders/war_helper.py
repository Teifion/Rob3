from pages import common
# from functions import oh_f
from classes import wh

page_data = {
	"Admin":	True,
	"Title":	"War helper",
	# "Headers":	True,
}

def main(cursor):
	team_id		= int(common.get_val('team', 0))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>%s" % (common.select_team_form(
			cursor, 'war_helper', dev_mode=1, ajax=1
		), common.onload("$('#select_team_input').focus();"))
	
	the_wh = wh.Wh(cursor)
	the_wh.local_path = True
	the_wh.setup()#true_team_list=[team_id])
	
	return the_wh.make_wh(team_id)