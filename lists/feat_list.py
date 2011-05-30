import database

category = [
	'Attack',
	'Ability',
	'Skill',
	'Aura',
	'Misc',
]

class Feat (database.DB_list_row):
	"""docstring for Building"""
	def __init__(self):
		super(Feat, self).__init__()
		self.set_values(max_level=3)
		self.set_values(category=0, feat_name="", description="")
	
	def check(self):
		pass

data_list = []
data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Power attack")
data_list[-1].set_values(category=category.index('Attack'))
data_list[-1].set_values(description="Your attack speed halves but your attack damage increses by 100%. Another 100% is added at each subsequent level so that when level 3 you will strike with 300%% more force.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Flurry attack")
data_list[-1].set_values(category=category.index('Attack'))
data_list[-1].set_values(description="Your attack power drops to a third of normal but your rate of attack increases by 100%%. Another 100%% is added at each subsequent level so that when level 3 you will attack 300%% faster.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Guarded attack")
data_list[-1].set_values(category=category.index('Attack'))
data_list[-1].set_values(description="Your attack speed is halved as is the force of your attacks. However, you ability to parry and block is increased by 100%%. Another 100%% is gained at each subsequent level meaning that when level 3 you will block and parry 300%% better than normal.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)


data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Sprint")
data_list[-1].set_values(category=category.index('Ability'))
data_list[-1].set_values(description="You can for up for up to 5 seconds run, jump and turn at twice the speed you normally do. This improves by 5 seconds per level so that when level 3 you can use the ability for 15 seconds. Sprint takes 30 minutes to recharge.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Dodge")
data_list[-1].set_values(category=category.index('Ability'))
data_list[-1].set_values(description="For up to 5 seconds you can dodge twice as swiftly as you normally do. This is improved by 20 seconds each level, when level 3 you can dodge like this for up to 60 seconds. Dodge takes 20 minutes to recharge.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Critical strike")
data_list[-1].set_values(category=category.index('Skill'))
data_list[-1].set_values(description="When using a piercing weapon you are able to halve your attack speed but become twice as accurate with your strikes. This becomes three times at level 2 and four at level 3. It also applies to using bows.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Cleaving blow")
data_list[-1].set_values(category=category.index('Skill'))
data_list[-1].set_values(description="When using a blunt weapon you are able to halve your attack speed but strike aim a swing so that it strikes an additional target infront of you. At level 2 you strike a 3rd and when level 3 you strike a fourth.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Deflect")
data_list[-1].set_values(category=category.index('Skill'))
data_list[-1].set_values(description="When using a slashing weapon you can halve your attack speed but double your ability to parry and when focusing on only this, blocking arrows. The ability becomes twice as good when level 2 and three times when level 3.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Aura of courage")
data_list[-1].set_values(category=category.index('Aura'))
data_list[-1].set_values(description="All allies within 100m of you have their maximum morale raised by 50%%. When level 2 this becomes 100%% and at level 3,  150%%.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Aura of endurance")
data_list[-1].set_values(category=category.index('Aura'))
data_list[-1].set_values(description="All allies within 100m of you have their maximum stamina raised by 50%%. When level 2 this becomes 100%% and at level 3, 150%%.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Aura of hesitance")
data_list[-1].set_values(category=category.index('Aura'))
data_list[-1].set_values(description="All enemies within 40m will hesitate 50%% logner before engaging in combat. When level 2 this becomes 100%% and at level 3, 150%%.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Chosen energy")
data_list[-1].set_values(category=category.index('Misc'))
data_list[-1].set_values(description="All attacks against special beings (first ones and giant beasts) become 50%% more powerful at no cost. When level 2 this becomes 75%% and when level 3, 100%%. Spells do not benefit from this.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1, feat_name="Hardiness")
data_list[-1].set_values(category=category.index('Misc'))
data_list[-1].set_values(description="Your toughness increases by 25%% at no cost. When level 2 this becomes 50%% and when level 3, 75%%.")

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)

data_list.append(Feat())
data_list[-1].set_values(id=len(data_list)-1)