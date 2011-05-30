from pages import common
from data import battle_q

battle	= int(common.get_val('battle', 0))
team	= int(common.get_val('team', 0))

# Make the call
battle_q.remove_team_from_battle(battle, team)

# Redirect
print("Location: edit_battle&battle=%s" % battle)