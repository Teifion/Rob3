from pages import common
from data import mission

# mission settings
the_mission = mission.Mission()
the_mission.get_from_form(common.cgi_form.list)
the_mission.update()

# Redirect
print "Location: latest_missions"