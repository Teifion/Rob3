import time, random
from pages import common
from data import mission_f

mission_id	= int(common.get_val("mission", 0))
losses		= common.get_val("loss", "").split(',')
info		= common.get_val("info", "")

if losses == ['']: losses = []


# Error checking
if info == "":
	print ""
	print "Error, no info was specified. Even a failed mission provides info."
	exit()

mission_f.handle_mission(mission_id, info, losses)

# Handle the next mission
print "Location: handle_mission"