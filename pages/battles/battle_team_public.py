from pages import common
from data import battle_q

team	= int(common.get_val('team', 0))
battle	= int(common.get_val('battle', 0))

battle_q.make_team_public(team, battle)