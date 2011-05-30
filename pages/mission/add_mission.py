import re
from pages import common
from data import mission_f

team			= int(common.get_val("team", 0))
turn			= int(common.get_val("turn", 0))
the_type		= int(common.get_val("type", 0))
state			= int(common.get_val("state", 0))
target			= int(common.get_val("target", 0))

mission_f.new_mission(team, turn, the_type, state, target)

# Redirect
print("Location: latest_missions")