from pages import common
from classes import player

page_data = {
	"Admin":	True,
	"Redirect":	"list_players",
}

def main(cursor):
	the_player = player.Player()
	the_player.get_from_form(common.cgi_form.list)
	the_player.update(cursor)
	
	return ""