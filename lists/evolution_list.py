import database
from data_classes import evolution

# categories = evolution.categories
cat_lookup = evolution.categories.index

class Evolution (database.DB_list_row):
	def __init__(self):
		super(Evolution, self).__init__()
		self.set_values(cost_per_level=1, max_level=10, min_level=-10)
		self.set_values(physical_change=0, combat_relevant=False)
	
	def check(self):
		pass

data_list = []
data_list.append(Evolution())
data_list[-1].set_values(name="Strength")
data_list[-1].set_values(physical_change=0.15, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Each level of this evolution causes your people to become 10% stronger. Strength refers to the muscular power of the body. Taken as a negative it will cause them to become 8% weaker.")

data_list.append(Evolution())
data_list[-1].set_values(name="Agility")
data_list[-1].set_values(physical_change=0.15, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Each level of this evolution causes your people to become 10% more agile. Agility refers to the flexibility and speed of the body. Taken as a negative it will cause them to become 8% less agile.")

data_list.append(Evolution())
data_list[-1].set_values(name="Toughness")
data_list[-1].set_values(physical_change=0.15, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Each level of this evolution causes your people to become 10% tougher. Toughness refers to the robustness of the flesh and organs of the body. Taken as a negative it will cause them to become 8% less tough.")

data_list.append(Evolution())
data_list[-1].set_values(name="Arm length")
data_list[-1].set_values(physical_change=3, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="The arms of your people extend by 6cm, taken as a negative they become 6cm shorter.")

data_list.append(Evolution())
data_list[-1].set_values(name="Leg length")
data_list[-1].set_values(physical_change=3, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="The legs of your people extend by 6cm, taken as a negative they become 6cm shorter.")


data_list.append(Evolution())
data_list[-1].set_values(name="Intellect")
data_list[-1].set_values(physical_change=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Mental'), description="Each level of this evolution causes your people to become 10% smarter and more intelligent. Intelligence allows your people to act better without your direct control. Taken as a negative it will cause them to become 8% stupider.")

data_list.append(Evolution())
data_list[-1].set_values(name="Aggression")
data_list[-1].set_values(physical_change=0.01, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Each level of this evolution causes your people to be able to control their anger and aggression better, to use it when it is needed yet to restrain it at other times. Taking this as a negative causes them to lash out in an unrestrained manner much more easily.")

data_list.append(Evolution())
data_list[-1].set_values(name="Perception")
data_list[-1].set_values(physical_change=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Mental'), description="This causes your people to be 15% better at observing and noticing things. Taken as a negative they become 10% worse. This applies mostly to situations involving subterfuge.")

data_list.append(Evolution())
data_list[-1].set_values(name="Willpower")
data_list[-1].set_values(physical_change=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Mental'), description="Your people become stronger willed, 5% more willpower per level or 5% less per level if taken as a negative.")

data_list.append(Evolution())
data_list[-1].set_values(name="Morale")
data_list[-1].set_values(physical_change=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Mental'), description="Each level causes the initial morale of your people in a given situation to be 10% higher or 5% lower if taken as a negative. It does not alter the rate at which morale rises and falls, just how much you have to start with.")

#	AFFINITIES
#------------------------
data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (General)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All spells cast by your mages have a 3% greater payload per level, be that damage, fireballs per second or some other metric. This ability does not carry over to enchantments.")

data_list.append(Evolution())
data_list[-1].set_values(name="Innately magical")
data_list[-1].set_values(cost_per_level=3)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Each level lowers the cost of mages by 0.01, this applies to all three tiers. At level 10 your low tier mages are priced only at 0.05 materials each.")

data_list.append(Evolution())
data_list[-1].set_values(name="Technological affinity")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Each level allows you to produce an extra 5% tech points or 5% fewer as a negative.")

data_list.append(Evolution())
data_list[-1].set_values(name="Affinity for war")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="The upkeep of your troops becomes 5% less per level or 10% more if taken as a negative.")

data_list.append(Evolution())
data_list[-1].set_values(name="Affinity for combat")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Your race become better at hitting people, well, there is a bit more to it than that but that is essentially it. Each level makes them 10% better at both melee combat and ranged combat. Taken as a negative they become 5% worse at it per level.")

data_list.append(Evolution())
data_list[-1].set_values(name="Natural riders")
data_list[-1].set_values(cost_per_level=2, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="The proficiency of the race in riding any beast is increased by 10%, this causes them to have more control over their mounts and to be able to breed them to a higher standard.")

data_list.append(Evolution())
data_list[-1].set_values(name="Population growth")
data_list[-1].set_values(cost_per_level=4)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Your population growth rate rises by 5% per level, that is the increase you normally have is made 5% bigger per level. Taken as a negative it reverses its effect and gives a 5% decrease.")

data_list.append(Evolution())
data_list[-1].set_values(name="Affinity for the waves")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Your race become 10% better at sailing ships and existing on the seas, taken as a negative it will lower this ability. A level 10 negative in this will mean that they will die if they take even a short voyage.")

data_list.append(Evolution())
data_list[-1].set_values(name="Affinity for the land")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Your race are able to grow 5% more food per level or 5% less food if taken as a negative.")

data_list.append(Evolution())
data_list[-1].set_values(name="Affinity for flight")
data_list[-1].set_values(cost_per_level=2, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Your race become 10% better at sailing airships and riding flying mounts.")

# Stuff that was added afterwards
data_list.append(Evolution())
data_list[-1].set_values(name="Charisma")
data_list[-1].set_values(cost_per_level=1)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Your people become 10% better at talking and bluffing per level. Taken as a negative and they become 10% worse.")

data_list.append(Evolution())
data_list[-1].set_values(name="Body size")
data_list[-1].set_values(cost_per_level=4, physical_change=20, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Your people grow 5% larger or smaller each level. With this comes a slight alteration to strength and toughness.")

data_list.append(Evolution())
data_list[-1].set_values(name="Loyalty")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Mental'), description="The loyalty of your people increases or decreases by 5%, they are less likely to defect and become subverted.")

data_list.append(Evolution())
data_list[-1].set_values(name="Extra arm")
data_list[-1].set_values(cost_per_level=10, min_level=0, physical_change=100, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Your race grow an extra arm. It is fully functional and doesn't impede the other limbs.")

data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (Light)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True, min_level=0)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All light spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric.")

data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (Dark)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True, min_level=0)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All dark spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric.")

data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (Destruction)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True, min_level=0)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All descruction spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric.")

data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (Abjuration)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True, min_level=0)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All abjuration spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric.")

data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (Daemonic)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True, min_level=0)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All daemonic spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric. This does not affect daemonic progression spells.")

data_list.append(Evolution())
data_list[-1].set_values(name="Magical affinity (Necromantic)")
data_list[-1].set_values(cost_per_level=2, combat_relevant=True, min_level=0)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All necromantic spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric.")

data_list.append(Evolution())
data_list[-1].set_values(name="VOID")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All necromantic spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric. This ability does not carry over to enchantments.")

data_list.append(Evolution())
data_list[-1].set_values(name="VOID")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="All daemonic spells cast by your mages have a 10% greater payload per level, be that damage, fireballs per second or some other metric. This ability does not carry over to enchantments.")

data_list.append(Evolution())
data_list[-1].set_values(name="Metabolic Efficiency")
data_list[-1].set_values(cost_per_level=3)
data_list[-1].set_values(category=cat_lookup('Physical'), description="5% less food is consumed by your people per level. 10% more is consumed should you take this as a negative.")

# data_list.append(Evolution())
# data_list[-1].set_values(name="Charisma")
# data_list[-1].set_values(cost_per_level=1)
# data_list[-1].set_values(category=cat_lookup('Affinity'), description="Your people become 10% better at talking and bluffing per level. Taken as a negative and they become 10% worse.")

data_list.append(Evolution())
data_list[-1].set_values(name="Height")
data_list[-1].set_values(cost_per_level=1)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Your race are 5cm taller per level or 4cm shorter if as a negative. Levels of this will produce either tall and lanky people or short and squat ones.")

data_list.append(Evolution())
data_list[-1].set_values(name="Endurance")
data_list[-1].set_values(cost_per_level=1, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="The stamina of your people grows or shrinks 5% per level.")

data_list.append(Evolution())
data_list[-1].set_values(name="Lung capacity")
data_list[-1].set_values(cost_per_level=1, physical_change=0.1, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="The lung capacity of your people grows 5% per level.")

data_list.append(Evolution())
data_list[-1].set_values(name="Extra leg")
data_list[-1].set_values(cost_per_level=10, min_level=0, physical_change=100, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Physical'), description="Your race grows an extra leg. It does not impede the other limbs.")

data_list.append(Evolution())
data_list[-1].set_values(name="Affinity for Economics")
data_list[-1].set_values(cost_per_level=2)
data_list[-1].set_values(category=cat_lookup('Affinity'), description="Material production rises or falls by 5% per level")

data_list.append(Evolution())
data_list[-1].set_values(name="Tough skin")
data_list[-1].set_values(cost_per_level=1, min_level=0)
data_list[-1].set_values(category=cat_lookup('Physical'), description="The skin of your people becomes tougher, at level 10 it is tougher than leather armour.")

data_list.append(Evolution())
data_list[-1].set_values(name="VOID")
data_list[-1].set_values(cost_per_level=1)
data_list[-1].set_values(category=cat_lookup('Physical'), description="")

data_list.append(Evolution())
data_list[-1].set_values(name="VOID")
data_list[-1].set_values(cost_per_level=1)
data_list[-1].set_values(category=cat_lookup('Physical'), description="")

data_list.append(Evolution())
data_list[-1].set_values(name="Religious fanatics")
data_list[-1].set_values(cost_per_level=2, min_level=0)
data_list[-1].set_values(category=cat_lookup('Mental'), description="A 30% increase to religious fevour, it is harder to sway them from the path of their patron deities.")


#	Radicals
#------------------------
data_list.append(Evolution())
data_list[-1].set_values(name="Regeneration")
data_list[-1].set_values(cost_per_level=17, max_level=1, min_level=0, physical_change=30, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="Your people are able to heal wounds in minutes (thus stopping the bleeding) and heal broken bones overnight, to re-grow a limb will take a couple of weeks of rest.")

data_list.append(Evolution())
data_list[-1].set_values(name="Second heart")
data_list[-1].set_values(cost_per_level=10, max_level=1, min_level=0, physical_change=5, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="Your people have a second heart providing an overall incrase to stamina and stamina recovery")

data_list.append(Evolution())
data_list[-1].set_values(name="IR Nightvision")
data_list[-1].set_values(cost_per_level=9, max_level=1, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="Your people are able to see heat sources and thus perform better in the dark")

data_list.append(Evolution())
data_list[-1].set_values(name="Fast clotting blood")
data_list[-1].set_values(cost_per_level=3, max_level=1, min_level=0, physical_change=10, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="")

data_list.append(Evolution())
data_list[-1].set_values(name="Waterproof fur")
data_list[-1].set_values(cost_per_level=3, max_level=1, min_level=0, physical_change=5)
data_list[-1].set_values(category=cat_lookup('Radical'), description="")

data_list.append(Evolution())
data_list[-1].set_values(name="Webbed feet")
data_list[-1].set_values(cost_per_level=3, max_level=1, min_level=0, physical_change=5)
data_list[-1].set_values(category=cat_lookup('Radical'), description="")

data_list.append(Evolution())
data_list[-1].set_values(name="Winged arms")
data_list[-1].set_values(cost_per_level=30, max_level=1, min_level=0, physical_change=100, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Avian species (feathers, hollow bones)
Bird like head, talons, tails, scaled hands and feet
Wings are connected to the arms and cannot be used separately
Physical evos lower flight ability (agility not included)
Enduranc boosts flight time
Cannot fly with armour or heavy items
Flight uses up more energy, troops flying require more supplies mid-campaign
Long distance travel is 2-5 times as fast as cavalry and flys in a straight line
Metabolic efficiency does not affect groups that constantly fly (unsupplied troops)""")

# Todo remove this evo as it's built from common ones
data_list.append(Evolution())
data_list[-1].set_values(name="Hardy dwarves")
data_list[-1].set_values(cost_per_level=6, max_level=1, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""4 foot tall and proportionately sized. 50% stronger than a human and with bones twice as tough.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Blood Reign")
data_list[-1].set_values(cost_per_level=6, max_level=1, min_level=0, physical_change=15, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Drinking fresh blood causes their body to repair itself at a very fast rate. It has a short term addictiveness that causes them to seek more blood.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Nightvision (Rods)")
data_list[-1].set_values(cost_per_level=8, max_level=1, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""A different ratio of cones and rods in the eyes, can see better in the dark but not so well in the light""")

data_list.append(Evolution())
data_list[-1].set_values(name="Flesh eaters")
data_list[-1].set_values(cost_per_level=3, max_level=1, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""After defeating a enemies in battle those with this evolution eat the flesh of the dead and bolster their morale and reduce the need to forage for food""")

data_list.append(Evolution())
data_list[-1].set_values(name="Calidi bone armour")
data_list[-1].set_values(cost_per_level=14, max_level=1, min_level=0, physical_change=50, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Sheets of bone on the arms, legs and torso. Bones are linked by bone ring-mail. Capable of withstanding hits from light weapons, little defense against heavy blows.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Giant eyes")
data_list[-1].set_values(cost_per_level=4, max_level=1, min_level=0, physical_change=40, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Their eyes are twice the radius of normal ones and can see far better both at day and night.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Ouchucia centigors")
data_list[-1].set_values(cost_per_level=26, max_level=1, min_level=0, physical_change=100, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Lower body of a horse with clawed feet and a goatish head
- 70% more strength, 40% more toughness, 20% more endurance, 40% more food consumed, 20% less agility""")

data_list.append(Evolution())
data_list[-1].set_values(name="Wyrmkin")
data_list[-1].set_values(cost_per_level=6, max_level=1, min_level=0, physical_change=30, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Red scaly skin (equal to leather armour) which is also flame retardant
- Long snout face with green/gold eyes""")

data_list.append(Evolution())
data_list[-1].set_values(name="Tapetum Lucidum")
data_list[-1].set_values(cost_per_level=8, max_level=1, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""A layer of reflective cells behind the retina that reflects all visiable light into the photoreceptors of the eyes. This improves their vision in low light conditions.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Eyes of the hunter")
data_list[-1].set_values(cost_per_level=4, max_level=1, min_level=0, physical_change=5, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""The pupils can expand to twice the width of a normal person's and retract to half the width of a normal person's. This allows them to adjust to changes in light levels twice as fast.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Shark skin")
data_list[-1].set_values(cost_per_level=2, max_level=1, min_level=0, physical_change=5)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Abrasive skin that provides less water resistance.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Green skin")
data_list[-1].set_values(cost_per_level=1, max_level=1, min_level=0, physical_change=5)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""""")

data_list.append(Evolution())
data_list[-1].set_values(name="Enhanced smell")
data_list[-1].set_values(cost_per_level=5, max_level=1, min_level=0, combat_relevant=True)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""The nose and tongue are packed with many times the number of smell receptors as a normal human and thus the sense of smell is far far more powerful.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Minotaurs")
data_list[-1].set_values(cost_per_level=4, max_level=1, min_level=0, physical_change=100)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Bull like legs, hooves at the end.
Short, coarse, fur that covers their entire bodies. About an inch long.
Bull like heads, including long horns. Foot long, slightly curved forward at the tip and sharp.""", combat_relevant=True)

data_list.append(Evolution())
data_list[-1].set_values(name="Resistance to pain")
data_list[-1].set_values(cost_per_level=2, max_level=10, min_level=-10, physical_change=0)
data_list[-1].set_values(category=cat_lookup('Physical'), description="""Your people become either 5% more resistant to pain or 15% more affected by it per level.""", combat_relevant=True)

data_list.append(Evolution())
data_list[-1].set_values(name="Inverted sabre teeth")
data_list[-1].set_values(cost_per_level=1, max_level=1, min_level=0, physical_change=3)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Massive fangs reaching from the lower lip to the the eyes.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Horns")
data_list[-1].set_values(cost_per_level=2, max_level=1, min_level=0, physical_change=20)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Horns sprout from the head, not an effective combat weapon""")

data_list.append(Evolution())
data_list[-1].set_values(name="Quadrapeds")
data_list[-1].set_values(cost_per_level=5, max_level=1, min_level=0, physical_change=15)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""The race can move on two legs or on all four""")

data_list.append(Evolution())
data_list[-1].set_values(name="Fur")
data_list[-1].set_values(cost_per_level=1, max_level=1, min_level=0, physical_change=10)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""The race is covered in short fur""")

data_list.append(Evolution())
data_list[-1].set_values(name="Fangs")
data_list[-1].set_values(cost_per_level=1, max_level=1, min_level=0, physical_change=10)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""""")

data_list.append(Evolution())
data_list[-1].set_values(name="Wolf tail")
data_list[-1].set_values(cost_per_level=3, max_level=1, min_level=0, physical_change=10)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""""")

data_list.append(Evolution())
data_list[-1].set_values(name="Vor'en Schifu cosmetic changes")
data_list[-1].set_values(cost_per_level=2, max_level=1, min_level=0, physical_change=10)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Long pointed ears, almond shaped eyes and a rainbow spectrum of skin colours.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Vaar'Shai cosmetic changes")
data_list[-1].set_values(cost_per_level=2, max_level=1, min_level=0, physical_change=10)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Grey skin and yellow eyes""")

data_list.append(Evolution())
data_list[-1].set_values(name="Soft regeneration")
data_list[-1].set_values(cost_per_level=10, max_level=1, min_level=0, physical_change=0)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""Limbs can be reattatched and even large wounds can be healed over time.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Ogoth form")
data_list[-1].set_values(cost_per_level=24, max_level=1, min_level=0, physical_change=100)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""The crocodile-headed Ogoth are a brutish and brutal race. The have four solid arms and a short tail, each a weapon in their own right. Small black eyes of death stare from their massive heads. Oozing strands of yellowish saliva drip from their long toothy maws. The voice of an Ogoth is a guttural, deep grumble. They speak rarely and never at length.""")

data_list.append(Evolution())
data_list[-1].set_values(name="Scales")
data_list[-1].set_values(cost_per_level=1, max_level=1, min_level=0, physical_change=10)
data_list[-1].set_values(category=cat_lookup('Radical'), description="""A thin plate of bone overlapping another thin plate of bone which in turn overlaps another thin plat of bone to form something akin to snake or fish scales, the bone overlapping bone scales are so thin it offers no extra protection.""")