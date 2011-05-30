from pages import common
from data import mission_q

mission_q.delete_mission(int(common.get_val('mission', -1)))

# Redirect
print('location:latest_missions')