import database
from lists import deity_list as deity_module

class Servant (database.DB_list_row):
	"""docstring for Building"""
	def __init__(self):
		super(Servant, self).__init__()
		self.set_values(favour_needed=1, temple_points=1)
		self.set_values(description="", monotheistic=False)
	
	def check(self):
		# Why show it if you can't summon it?
		self.temple_points = max(self.temple_points, self.summon_cost)
	

# Maybe not the coolest way to do it but it saves issues later
deity_list = []
for d in deity_module.data_list:
	deity_list.append(d.name)

# deity_list = [
# 	'Arl',
# 	'Trchkithin',
# 	'Adyl',
# 	'Ssai',
# 	'Orakt',
# 	'Agashn',
# 	'Ldura',
# 	'Azmodius',
# 	'Phraela and Caist',
# 	'Soag chi',
# 	'Khystrik',
# 	'Laegus',
# ]

data_list = []

# Arl
data_list.append(Servant())
data_list[-1].set_values(name="Cherub", deity=deity_list.index("Arl"))
data_list[-1].set_values(favour_needed=1, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=20)
data_list[-1].set_values(description="A small being looking like a human infant but with small wings. It has a a bow and can fire with amazing accuracy. Their agile form is problematic for almost any other flier though their physical form is very vulnerable to all attacks.")

# Trchkithin
data_list.append(Servant())
data_list[-1].set_values(name="Harbinger", deity=deity_list.index("Trchkithin"))
data_list[-1].set_values(favour_needed=4, temple_points=4)
data_list[-1].set_values(summon_cost=1, summon_amount=1, monotheistic=True)
data_list[-1].set_values(description="A winged centaur type beast, it's body is infused with destructive energies which it channels through a pair of scepters. At range the scepters unleash a bolt of energy that explodes in a shockwave of kinetic force, in combat the scepters can smash apart even the thickest of plate.")

# Adyl
data_list.append(Servant())
data_list[-1].set_values(name="Protector", deity=deity_list.index("Adyl"))
data_list[-1].set_values(favour_needed=2, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=10)
data_list[-1].set_values(description="A sealed suit of plate mail weidling a long sword and large shield, the body of the creature is made from water. Denting the armour does little to slow the tireless entity, instead you must puncture it and allow the daemonic spirit to drain from the armour.")

data_list.append(Servant())
data_list[-1].set_values(name="Absolution Knight", deity=deity_list.index("Adyl"))
data_list[-1].set_values(favour_needed=1, temple_points=4)
data_list[-1].set_values(summon_cost=1, summon_amount=10)
data_list[-1].set_values(description="A mounted knight brought back from the dead to continue defending the weak. They know no fear and are nearly impervious to all ranged attacks, both magical and mundane and are also armoured in full plate atop a barded warhorse.")

# Ssai
data_list.append(Servant())
data_list[-1].set_values(name="Voidstalker", deity=deity_list.index("Ssai"))
data_list[-1].set_values(favour_needed=2, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=4, monotheistic=True)
data_list[-1].set_values(description="The Voidstalker is almost invisible to the naked eye, a permanent chameleon spell provides a slight refraction of light as it moves, it has no breath and no body heat so is almost impossible to detect. The shape of a void stalker is almost identical to that of a snake, the main difference being the slight levitation of a Void Stalker. The Void stalker does not engage itself in combat directly, it is far too weak for that. Instead it watches from the shadows, reading the minds of one person at a time and forwarding the information on to the faithful of Ssai.")

data_list.append(Servant())
data_list[-1].set_values(name="Shade", deity=deity_list.index("Ssai"))
data_list[-1].set_values(favour_needed=1, temple_points=2)
data_list[-1].set_values(summon_cost=1, summon_amount=8)
data_list[-1].set_values(description="Nimble warriors, smaller and weaker than a human but with the ability to momentarily drop out of phase and pass through phsyical objects. A competent assassin though not of much use on the field of battle.")

# Orakt
data_list.append(Servant())
data_list[-1].set_values(name="Red blades", deity=deity_list.index("Orakt"))
data_list[-1].set_values(favour_needed=2, temple_points=4)
data_list[-1].set_values(summon_cost=4, summon_amount=50)
data_list[-1].set_values(description="Orakt has as his personal guard a group of daemons called Red Blades, they are humanoid but twice the size of a human and with an unnatural skill for fighting. They wield halberds and fight in a formation with a coordination matched only by Cyrgai. Each Red blade within 1m of any other will give each a 5% boost to their strength.")

# Agashn
data_list.append(Servant())
data_list[-1].set_values(name="Krogoth", deity=deity_list.index("Agashn"))
data_list[-1].set_values(favour_needed=4, temple_points=4)
data_list[-1].set_values(summon_cost=10, summon_amount=1, monotheistic=True)
data_list[-1].set_values(description="Given by Agashn as a gift to his most devout followers only. Krogoths are humanoid, big and nasty. Covered in a thick fur and towering over anything else the Krogoth will typically tip any battle in favour of Agashn. Agashn values his power and the blessing of a 12m tall daemon is given only to his most devout and favoured servants.")

# Ldura
data_list.append(Servant())
data_list[-1].set_values(name="Arcane lanterns", deity=deity_list.index("Ldura"))
data_list[-1].set_values(favour_needed=2, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="A brain supported by a single tentacle, the lanterns are not a scary force. They possess prodigious senses and can see things through all open minds around them. Lanterns possess no abilities of war but are amazing observers and used well can provide invaluable information.")

# Azmodius
data_list.append(Servant())
data_list[-1].set_values(name="Pyronath", deity=deity_list.index("Azmodius"))
data_list[-1].set_values(favour_needed=1, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=30)
data_list[-1].set_values(description="Pyronaths are screaming horrors. Their exact shape is unknown as all that can be seen of them is a ball of fire. The Pyronath has no apparent physical strength, it does not need it. They burn with a yellow flame normally, however, in the presence of enough magic they will burn a turquoise colour, and violently at that. Their only method of attack is to explode, they are practically immune to mundane attacks, magic only makes them burn harder (enough of it and they'll explode). They typically cover an area of 10m with their yellow blast, and an area of 20m or more when sustained by magic.")

data_list.append(Servant())
data_list[-1].set_values(name="Zelot", deity=deity_list.index("Azmodius"))
data_list[-1].set_values(favour_needed=3, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=8, monotheistic=True)
data_list[-1].set_values(description="Zelots are for all apperances human yet magical energy cannot affect them and any magical energy that does come into contact them will ignite. Zelots are able to sense the location of mages and will hunt them down with vigour.")

# Phraela and Caist
data_list.append(Servant())
data_list[-1].set_values(name="Gaunt", deity=deity_list.index("Phraela and Caist"))
data_list[-1].set_values(favour_needed=1, temple_points=4)
data_list[-1].set_values(summon_cost=1, summon_amount=24)
data_list[-1].set_values(description="Gaunts appear completely human. They carry a pike, wear a brestplate and always come in large numbers. They fight in a phalanx and always as one unit. Their minds are all completely linked and as such the formation is able to achieve things impossible even for Cyrgai. Gaunts are only slightly stronger than humans.")

data_list.append(Servant())
data_list[-1].set_values(name="Sword and shield", deity=deity_list.index("Phraela and Caist"))
data_list[-1].set_values(favour_needed=3, temple_points=2)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="Always summoned as a pair, one is a group of floating swords and the other a group of floating shields, each actually being a small hovering daemon holding the items up. When paired the sword is strong and can cut through plate, when not paired it will be unable to pierce any armour. When paired the Shield is tough and will regenerate, when not paired it will crack and not regenerate.")

# Soag chi
data_list.append(Servant())
data_list[-1].set_values(name="Arbasque", deity=deity_list.index("Soag chi"))
data_list[-1].set_values(favour_needed=3, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=2, monotheistic=True)
data_list[-1].set_values(description="Arbasque are strange beings, they appear as an aged human woman with a ghastly complextion and horrified face. They possess little strength, endurance and no ability beyond their shriek. The shriek drives thoughts of others and unity from the minds of all that hear it. It does not cause people to attack their allies but it does destroy the communication and teamwork present in formations.")

# Khystrik
data_list.append(Servant())
data_list[-1].set_values(name="Seer", deity=deity_list.index("Khystrik"))
data_list[-1].set_values(favour_needed=3, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="Seers are not the sole property of Kyhstrik, it's thought that he stole some from Yspethc and has been since using them as if they are his own. The seer is a tall but hunched figure, very thin but to the untrained eye undoubtedly human. Seers have telepathic abilities, they possess very strong powers of mind reading (but not altering), they are however limited to a range of about a twenty meters, however, any mental magic that connects to them will provide a bridge that they can cross into the mind of an enemy. Seers tend to remain around far longer than most other servants and have been known to supply information to followers of Khystrik long after they were thought to have returned to their master.")

# Laegus
data_list.append(Servant())
data_list[-1].set_values(name="Burkastone", deity=deity_list.index("Laegus"))
data_list[-1].set_values(favour_needed=2, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="A mound of dirt and stone, it moves at a snail's pace yet is impossible to slay with conventional weaponry. The Burkastone is of no use in a battle yet in a siege is able to slowly pull apart a section of wall over several days. It is strongly advised that you summon it close to the target.")

# Alki
data_list.append(Servant())
data_list[-1].set_values(name="Bane elemental", deity=deity_list.index("Alki"))
data_list[-1].set_values(favour_needed=0, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="A centaur the size of a horse with four arms each holding a blade. Bane elementals are very strong and posses the energy field ability. Bane elementals grow 10% larger per temple point.")

# Zasha
data_list.append(Servant())
data_list[-1].set_values(name="Hunter killer", deity=deity_list.index("Zasha"))
data_list[-1].set_values(favour_needed=-1, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="They resemble a mantis like creature the size of a human but are very weak, a staff can easily break one of their spindly legs. They are however very fast, agile and also cunning. They can also track, but cannot fly. Hunter killers have the ability to smell magic and to track mages. Hunter killers cannot be detected magically and can sense the immediate future by 0.1 second per temple point.")

data_list.append(Servant())
data_list[-1].set_values(name="Nightbringer", deity=deity_list.index("Zasha"))
data_list[-1].set_values(favour_needed=-1, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="The Nightbringer Daemon is a very specialised Daemon. During the day it is but as strong and agile as a human. However, at Night it gains a 20% boost to strength and agility per temple point. Additionally it gains the ability to fly on wings of darkness. The Nightbringer is completely black, on a moonless night it is nigh on invisible because of this.")

data_list.append(Servant())
data_list[-1].set_values(name="Martel", deity=deity_list.index("Zasha"))
data_list[-1].set_values(favour_needed=-1, temple_points=1)
data_list[-1].set_values(summon_cost=1, summon_amount=1)
data_list[-1].set_values(description="The Martel is an unassuming daemon, it's immune to any form of scrying and is impossible to detect with magic. They are immune to spells such as banishment and energy field abilities yet posses double the strength, agility and toughness of a human. Martel gain an additional 5% size per temple point.")



for s in data_list:
	s.check()