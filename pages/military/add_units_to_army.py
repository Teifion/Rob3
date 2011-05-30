from pages import common
from data import army_f, army_q

team	= int(common.get_val("team", 0))
unit	= int(common.get_val("unit", 0))
amount	= int(common.get_val("amount", 0))
army	= common.get_val("army", 0)

if army == "XYZ_all_armies":
	army_list, armies_dict = army_q.get_armies_from_team(team=team, include_garrisons=1)
	
elif army == "XYZ_all_non_garrisons":
	army_list, armies_dict = army_q.get_armies_from_team(team=team, include_garrisons=0)
	
elif army == "XYZ_all_garrisons":
	army_list, armies_dict = army_q.get_armies_from_team(team=team, include_garrisons=-1)
	
else:
	# They have actually given us the ID of the army
	army_list = [army]

amount_per_army = amount/len(army_list)

for a in army_list:
	army_f.add_units_to_army(unit_type=unit, army_id=a, amount=amount_per_army)

# Redirect
if len(army_list) > 0:
	print("Location: list_armies&team=%s" % team)
else:
	print("Location: view_army&army=%s" % army_list[0])