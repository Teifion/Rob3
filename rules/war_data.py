# import database

damage_types = ["blunt", "pierce", "slash", "heat", "cold", "electrical", "chaos", "soul",]
armour_types = ["leather", "hide", "bone", "chain", "plate", "wood", "stone", "ethereal",]

# Shortcut to save on code
a = armour_types


damage_table = {
# 				leath	hide	bone	ch		pl		wo		st		et
"blunt":		[0.5,	0.75,	0.75,	0.5,	1.0,	1.0,	1.0,	0.0],
"pierce":		[1.0,	0.75,	1.0,	0.8,	0.25,	0.5,	0.75,	0.0],
"slash":		[0.75,	0.5,	0.25,	0.5,	0.5,	1.0,	0.75,	0.0],
"heat":			[1.0,	0.8,	1.0,	0.5,	0.75,	1.0,	0.15,	0.5],
"cold":			[0.75,	0.5,	1.0,	1.0,	1.0,	0.5,	0.15,	0.0],
"electrical":	[0.5,	0.25,	0.1,	1.0,	1.0,	0.15,	0.0,	0.25],
"chaos":		[1.0,	1.0,	1.0,	1.0,	1.0,	1.0,	1.0,	1.0],
"soul":			[1.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0.0,	1.0],
}