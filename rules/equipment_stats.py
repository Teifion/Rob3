# What they're good at, where they're a good choice, who they're effective against, etc. would be nice...

the_stats = {
	#	SWORDS
	#------------------------
	"Short sword": {
		"damage":		"Pierce",
		"range":		0.5,
		"one handed":	True,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Fast",
		
		"description":	"""A short and sharp blade, it is most effective when stabbing and due to it's small size is very effective when you can get right up against the enemy.""",
	},
	
	"Long sword": {
		"damage":		"Pierce/Slash",
		"range":		0.75,
		"one handed":	True,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""A good sized blade that can be used one or two handed for slashing or stabbing. It is a very versatile weapon""",
	},
	
	"Great sword": {
		"damage":		"Slash",
		"range":		1,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""A huge and cumbersome weapon. Though it can deal damage simply through the force of the blow it is often sharp and deadly against all types of armour.""",
	},
	"Twin swords": {
		"damage":		"Pierce/Slash",
		"range":		0.7,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Fast",
		
		"description":	"""A pair of swords generally a little shorter than the long sword to allow easier movement. It requires more skill to use two weapons at a time but the benefits can pay off.""",
	},
	
	#	AXES
	#------------------------
	"Axe": {
		"damage":		"Slash",
		"range":		0.5,
		"one handed":	True,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""A small and simple shaft of wood with a metal or even stone head. Slower and less balanced than a short sword the axe is however easier to use with little or no training.""",
	},
	"Great axe": {
		"damage":		"Slash",
		"range":		0.85,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""A pole with a huge axehead on it, sometimes two. It is heavy, cumbersome but effective against anything it can hit.""",
	},
	"Twin axes": {
		"damage":		"Slash",
		"range":		0.5,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Fast",
		
		"description":	"""Two small and fast axes. They require skill to use well but can be very effective.""",
	},
	#	BLUNT
	#------------------------
	"Mace": {
		"damage":		"Blunt",
		"range":		0.75,
		"one handed":	True,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""A pole with a large and blunt head on the end. It is cumbersome but heavy enough that it can damage the heaviest armour and batter away shields.""",
	},
	"Twin maces": {
		"damage":		"Blunt",
		"range":		0.7,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""Very hard to use and generally reserved for elite guards who will both have the training and formation to use them.""",
	},
	"Hammer": {
		"damage":		"Blunt",
		"range":		1,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""Huge and slow. Very effecitve against heavy armour and larger beasts.""",
	},
	"Flail": {
		"damage":		"Blunt",
		"range":		1.5,
		"one handed":	True,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""A chain connects the handle to the weighted head allowing for powerfun swings. Though much lighter than a hammer it can achieve similar or greater force but with far less effort. Flails completely obliterate shields but are useless in when close to the enemy.""",
	},
	#	POLEARMS
	#------------------------
	"Spear": {
		"damage":		"Pierce",
		"range":		2,
		"one handed":	True,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Fast",
		
		"description":	"""Simple and easy to use. Spears keep the enemy away from you, work very well in tight formation and provide enough reach for infantry to fight cavalry effectively.""",
	},
	"Pike": {
		"damage":		"Pierce",
		"range":		4,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Pikes are enourmous yet light weapons. Due to the length of the weapon even the light yet sharp head can weigh lot and to use a pike effectively you will need two hands. Pikes are very effective in tight formation and against cavalry but find it hard when flanked or when the enemy manages to get inside the reach of the pikes.""",
	},
	"Halberd": {
		"damage":		"Blunt/Pierce/Slash",
		"range":		1.5,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""A large staff with an axe-like head, a spear tip and often a blunt head too. Halberds are effective against many types of armour and weapon yet ineffective when up close or against spears and pikes.""",
	},
	"Lance": {
		"damage":		"Pierce",
		"range":		2,
		"one handed":	True,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Long, light and flimsy. Lances are designed to shatter after a few impacts and free up the knight for use of a different weapon. Lances are only effective when moving at speed and used only by cavarly. Lances are constructed before each battle and the cost is completely training related.""",
	},
	#	BOWS
	#------------------------
	"Shortbow": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Small and able to be used while jogging or riding. It's easy to make and easy to use against large numbers of targets.""",
	},
	"Bow": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Large enough that it's hard to use from a horse but able to be used while walking or in a chariot. It provides more range than a shortbow.""",
	},
	"Longbow": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Large range and with training a high rate of fire. It can only be used while stationary and with enough space. It provides more range than a standard bow.""",
	},
	"Composite bow": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""The size of a shortbow but with more power than a standard bow. Composite bows are harder to pull back but give cavalry the option of a more powerful bow. Infantry are generally better off using a shortbow, bow or longbow.""",
	},
	
	#	CROSSBOW
	#------------------------
	"Crossbow": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""Crossbows shoot small metal bolts and provide much more power than even a longbow. Crossbows are effective against heavier armour but take a lot longer to reload and are practically useless unless stationary.""",
	},
	"Repeating crossbow": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Fast",
		
		"description":	"""Reloaded by a lever the repeating crossbow has a very high rate of fire. It shoots wooden arrows so does not have the armour piercing capability of a normal crossbow, it is however very effective when used from a horse.""",
	},
	"Arbalest": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Arbalests are made completely from metal and thus suffer no ill effects from rain. They fire with more power than a crossbow and are effective against nearly all targets.""",
	},
	
	#	GUNPOWDER
	#------------------------
	"Musket": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	False,
		"two handed":	True,
		
		"weight":		1,
		"speed"	:		"Slow",
		
		"description":	"""Slow to reload, cumbersome to use and completely usless from horseback. Muskets are however very effective against light armour at medium range and heavy armour at short range. They require little training to use and are relatively cheap to produce. They are completely ineffective in the wet.""",
	},	
	#	THROWN
	#------------------------
	"Javelins": {
		"damage":		"Pierce",
		"range":		100,
		"one handed":	True,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Also goes by the name of pilum, throwing spear and many others. Essentially a shaft of wood with a pointed tip. Easy to use, great for skirmishers but not effecitve against heavy armour or large shields.""",
	},
	"Slings": {
		"damage":		"Slash",
		"range":		100,
		"one handed":	True,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Light, easy to use and cheap to boot. They are however short ranged, run out of ammunitition quickly and ineffective against heavy armour.""",
	},
	
	#	ARMOUR
	#------------------------
	"Leather jacket": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Thin yet flexible armour. It stops very littl, it's main use being to help against light weapons. Covers just the torso.""",
	},
	"Leather suit": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Thin yet flexible armour. It stops very littl, it's main use being to help against light weapons. Covers the torso, arms, legs and head.""",
	},
	"Chainmail jacket": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Metal rings chained together provide good protection against slashing attacks but can be vulnrable to stabbing attacks at they pass through the rings. Covers just the torso.""",
	},
	"Chainmail suit": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Metal rings chained together provide good protection against slashing attacks but can be vulnrable to stabbing attacks at they pass through the rings. Covers the torso, arms, legs and head.""",
	},
	"Banded armour jacket": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Strips of metal held together provide protection against slashing attacks and piercing attacks, a good all around armour. It covers just the torso.""",
	},
	"Banded armour suit": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Strips of metal held together provide protection against slashing attacks and piercing attacks, a good all around armour. It covers the torso, arms, legs and head.""",
	},
	"Breastplate": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""A solid piece of metal provides high restance to all but the most forceful of blows. Covers just the torso.""",
	},
	"Full plate suit": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Solid plates of metal are slow and cumbersome but make one nearly completely immune to anything but the heaviest of strikes. Covers the entire body.""",
	},	
	#	SHIELDS
	#------------------------
	"Buckler": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""A small rim of wood and sometimes metal provides little impediment to the movements of the bearer but also provides only a little defense and then only in combat.""",
	},
	"Small shield": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Light and easy to use, it provides some protection against arrows and decent protection in combat.""",
	},
	"Large shield": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Large enough to use in a shieldwall and to provide good protection from arrows. Harder to use in combat than a small shield but can block much heavier blows.""",
	},
	"Tower shield": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Large and rectangular it is perfect for shieldwalls and formational fighting. It works well as long as the line holds but in messier combat it is more an encumbrance than a defense.""",
	},	
	#	Centaur armour
	#------------------------
	"Centaur leather": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Centaur chainmail": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Centaur plate": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},	
	#	MOUNTS
	#------------------------
	"Horse": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Common, fast and agile.""",
	},
	"Warhorse": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Much larger than a horse it is excellent for charging enemy infantry.""",
	},
	"Barded warhorse": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Metal sheets draped down the side of the warhorse make it much more resistant to arrows and remove it's biggest weakness.""",
	},
	"Etiwcem": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""The Etiwcem is about twice the height of a human and 4 metres long. It resembles a bear in colour and texture but the fur is much longer. It has 8 legs on each side and can shuffle along slowly. They are strong but not fast nor tough. Etiwcem are found all over the world. Typically only a small herd will be captured in one area. 6 humans can fit atop a single Etiwcem.""",
	},
	
	
	"Barded etiwcem": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Identical to an Etiwcem but with sheets of metal down the side to protect against arrows.""",
	},
	"Mules": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Not battle-worthy like a horse but provide a faster march speed""",
	},
	
	"Camel": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Slower and less agile than a horse but more aggressive. Horses are afraid of camels. Camels also have much higher stamina than horses and are ideal for desert fighting.""",
	},
	
	"Barded camel": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Camels use leather barding to allow for better use in the desert.""",
	},
	
	"Pegasus": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are essentially a flying pony. Pegasai are very frail and cannot carry much more weight than a human, they are docile and exist over most of the world. It is possible to catch small herds of Pegasai in one area.""",
	},
	
	"Vizzig": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are akin to giant ducks but without the wings and weak bone structure. With giant webbed feet the Vizzig make fighting in a swamp possible. They can support the weight of people with armour but wearing such a thing in a swamp is a bad idea, if you fall off the Vizzig you will surely die. Vizzig are found in swamps and on the banks of rivers all around the world. They eat mainly grass and make poor fighters. It is easy to catch entire herds of Vizzig in one area.""",
	},

	"Large chariot": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	#data_list[-1].set_values(description="A 4 man chariot")

	"Large chariot with barded warhorses": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	#data_list[-1].set_values(description="A 4 man chariot")

	"Medium chariot": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	#data_list[-1].set_values(description="A 3 man chariot")

	"Medium chariot with barded warhorses": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	#data_list[-1].set_values(description="A 3 man chariot")

	"Small chariot": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	#data_list[-1].set_values(description="A 2 man chariot")

	"Small chariot with normal horses": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	#data_list[-1].set_values(description="A 2 man chariot")
	
	#	SIEGE ENGINES
	#------------------------
	"Catapult": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Mangonel": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Onager": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Scorpion": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Ballista": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Trebuchet": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},	
	#	BOAT HULLS
	#------------------------
	"Small craft": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Longship": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"100 tonne hull": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"250 tonne hull": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"400 tonne hull": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"600 tonne hull": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"800 tonne hull": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"1000 tonne hull": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},
	"Horse transport": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""""",
	},	
	#	Beasts
	#------------------------
	"Semyrid": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are giant winged birds, they have been described as bears with wings. Indeed, they have the body of a bear and with a wingspan capable of making short flights. Semyrid are violent creatures but respect strength.""",
	},

	"Peyam": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Giant flying beasts, their hide is like clay and hard to cut with swords. They posses two limbs just below the wing joints, these end in claws capable of ripping a man in two, it's hind legs are thick as trees and capable of supporting it's weight. Peyam are approximately 4m from head to the base of the tail, the tail itself is another 4m in length and ends in a giant club-link growth of bone. Peyam cannot fly long distances.""",
	},

	"Omhettri": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are about the size of a bear and resemble nothing more than a mass of fur. Omhettri however possess 12 "limbs" that appear to be a cross between a normal arm or leg and a tentacle. The limbs are about a metre in length and capable of pummeling a man to death. Omhettri have a mouth on their underside, they swallow their prey and digest every single part of them, they have been known to spit out people wearing metal armour. 
		
		The most astounding thing about the Omhettri is that they can regenerate. "Limbs" grow back after a couple of days and even removing large portions of their main body will grow back in weeks. All their vital organs have redundant copies of themselves so the only way to kill an Omhettri is to completely carve it apart until it dies. Omhettri are found in hilly areas, normally hiding to avoid detection. Capturing Omhettri is hard but it can be done, generally only one is captured at a time in an area.""",
	},

	"Qenki Wolves": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are half a meter longer than normal wolves and bulkier to keep in proportion. Their mouths are disproportionately large and they are capable of swallowing teenage humans. They are similar to wolves in every other way, their strength and endurance scaling up with their size but their speed and agility scaling down. They are found wherever there is food for them to eat, they live in packs. It is possible to capture entire packs in one area.""",
	},
	
	"Murtnk": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are a snake-like creature with a most amazing ability, they can wrap shadows around them to give them shape. While a Murtnk is in the shadow of the sun it will take on whatever appearance it chooses. Murtnk in reality are approximately 8 feet long and generally move with 4-6ft of their body held upwards. Their bite has a poison that enters the bloodstream and renders a victim unconscious.""",
	},
	
	"Enkny": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are giant humans, however, they are lanky and their knuckles drag along the floor, giving the impression that they are stupid, they are not. Enkny fashion spears and are very good at hunting with them, they can throw far and accurately. Enkny primarily live anywhere there is enough for them to eat but never living near Fidwy or Humans if they can help it. It is easy to catch small groups of Enkny in one area.""",
	},
	
	"Gorquithur": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""They are a creature that looks like it was designed as a weapon of war by some race long forgotten. Gorquithur are simply bears with boney spines protruding from the back of their limbs, head and body; much like a hedgehog. Gorquithur have a massive appetite and can run very fast for short distances of time. They are also stronger than bears but not by a lot. Very temporary friendship with a Gorquithur can be bought with food. Gorquithur are found only in small numbers.""",
	},
	
	"Grak beetles": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Grak beetles are like massive water bugs. They congregate along the shores of the Indrin isle, conveniently within the territories of the kliktaren. The creatures look much like blue-shelled wide-bodied beetles possessing six-legs. At the ends of the legs are webbed claws that they use to propel themselves through the water and they can dive under as well. They have compound eyes that enable them to see underwater as well as out of water. They have grinding mandibles they use to consume small fish and seaweed as well as plants and cacti. Grak beetles can breathe underwater.""",
	},
	
	"Toruk bugs": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""Toruk bugs are fairly sedentary insectoid creatures that have a number of physical characteristics that aren't typical of a giant bug. They have a course, shaggy fur that grows from their exoskeleton at the neck, back and lower thorax. They have six legs and wide, multi-eyed heads with tusk-like mandibles jutting from an oversized lower jaw. They naturally form herds and reside in the same regions near many Kliktaren hive cities and roving tribes. Toruk bugs are only hostile when their tribal brethren are threatened or their herd is in danger. They will attempt to trample or gouge aggressors but ultimately will do this to drive them away or to get away themselves.""",
	},
	
	"Drake wasps": {
		"damage":		"Slash",
		"range":		0,
		"one handed":	False,
		"two handed":	False,
		
		"weight":		1,
		"speed"	:		"Average",
		
		"description":	"""These are 3 or 4m long insectoid creatures with some oddly draconian aspects, particularly in the head and along the vertebrae. They have small claws too that look like they belong on a drake instead of an insect. The eyes look like slightly larger drake eyes but still compound like an insect and their backs have a definite spiky ridge all the way to the tail. These features are even more pronounced in the Warriors and Queens.""",
	},
}