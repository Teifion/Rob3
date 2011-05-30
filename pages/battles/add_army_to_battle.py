from pages import common
from data import battle_q

army	= int(common.get_val('army', 0))
battle	= int(common.get_val('battle', 0))

battle_q.add_army_to_battle(army, battle)

print('location:edit_battle&battle=%s' % battle)