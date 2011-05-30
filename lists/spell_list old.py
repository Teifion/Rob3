import database
from data_classes import spell

class Spell (database.DB_list_row):
	def __init__(self):
		super(Spell, self).__init__()
		self.set_values(max_level=10, description="")
		self.set_values(cooldown=0, cast_time=0)
		self.set_values(tradable=True)
	
	def check(self):
		# Empty advanced blocks = not what we want
		self.description = self.description.replace('\n\n<div class="advanced">\n\t\n</div>', "")

find_tier = spell.tiers.index
find_cat = spell.categories.index

data_list = []
data_list.append(Spell())
data_list[-1].set_values(name="Burning light")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=2*60, cast_time=2)
data_list[-1].set_values(description="""A beam of burning light is projected from the palm of the caster's hand. It disperses at an angle of 10 degrees, by the time it has reached 100m it is so weak as to be mostly just an annoyance. At 10m the light will cause sunburn instantly and burn through a ribcage in seconds. At a range of 50m it can burn through armour and bone within minutes. Each level increases the power by 20%. The spell lasts up to 1 minute and requires the concentration of the caster.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Tongue of Fire")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=2*60, cast_time=1)
data_list[-1].set_values(description="""A jet of flame is created from the caster's hand, it's hot enough to kill within seconds. The jet reaches 5m plus an additional metre per level. The spell lasts up to 1 minute and requires the concentration of the caster.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Embolden")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=5)
data_list[-1].set_values(description="""Up to 1 target per level becomes unwavering in their resolve and will not flee. The spell lasts for an hour but requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Armour of Light")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=4*60, cast_time=5)
data_list[-1].set_values(description="""The target's armour begins to glow and shine with light. The armour becomes 30% tougher per level and causes all actions to use 7.5% less energy than normal. The spell lasts 1 hour and requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Dazzle")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=20, cast_time=1)
data_list[-1].set_values(description="""A short lived light but exceedingly bright light is created in the palm of the caster's hand. It shines so brightly that if cast from an airship above an area it will turn night into day directly below it. The spell lasts one second per level but requires no concentration to maintain.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Boost")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=2*60, cast_time=2)
data_list[-1].set_values(description="""The physical abilities of the target are doubled, they can run twice as fast, jump twice as high and suchlike. The spell lasts for 10 seconds per level but requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Create air/water")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=4*60, cast_time=5)
data_list[-1].set_values(description="""Water pours from the caster's hand at a rate of 10 litres every second. Alternately air may be created at the same rate or either water or air may be sucked away at that rate. The spell lasts one second per level and requires the concentration of the caster.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Create stone/metal")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=40*60, cast_time=30)
data_list[-1].set_values(description="""A sphere of metal or stone is created between the caster's hands. The sphere will be 1 litre in volume per level. Different types of stone may be created or any of the metals in the following list: Magnesium, Aluminium, Nickel, Iron, Tin, Copper, Lead, Mercury, Tungsten and Osmium. The spell takes ten seconds to complete and requires full concentration all the way through. You are unable to use this spell as a supply of Stone or Iron. You do not need to create a sphere specifically, you can cut parts out of it to form specific shapes that fit inside this sphere.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Bless")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=20*60, cast_time=5)
data_list[-1].set_values(description="""Up to 40 targets become blessed by light magic. They become 3% stronger per level and all actions require 2% less energy to perform per level. The spell lasts for 1 hour but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="United in Strength")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=15*60, cast_time=5)
data_list[-1].set_values(description="""Two targets per level have their strength increased by 200%. The spell lasts for an hour but requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Destroy Illusions")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=6*60, cast_time=3)
data_list[-1].set_values(description="""All illusionary creations within 50m of the caster are destroyed. Destroy Illusions will only destroy illusions of the same level or below it, level 5 destroy illusions will not counteract invisibility level 6. For the purposes of this spell "illusions" refers to any magically created image or distortion such as invisibility or dazzle.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Terrifying blaze")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=12*60, cast_time=5)
data_list[-1].set_values(description="""All enemy troops that come within 10m of the caster per level will see the caster as a terrifying and blazing apparition. Better trained troops or those with higher morale will feel less effect from this as will those in a strong defensive position. Multiple mages with the Terrifying blaze spell in effect will provide more terror but with diminishing returns. The spell lasts 30 minutes but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Blazing Flare")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=4*60, cast_time=3)
data_list[-1].set_values(description="""A bright ball of fire is blasted forwards by the caster, it travels on a flat trajectory and after 50m plus 10m per level will explode in a bright ball of light and slowly fall to the ground. If it strikes a target before exploding it will explode early and probably melt whatever armour they are wearing along with giving very serious burns to those around them.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Cleanse")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=2*60, cast_time=5)
data_list[-1].set_values(description="""Up to 30 targets have all enemy spells removed from them. Cleanse can only remove spells that are of the same level or lower than it. The spell takes 5 seconds to cast and requires full concentration during this period.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Beacon")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=2*60*60, cast_time=60)
data_list[-1].set_values(description="""The tip of the caster's weapon or the tip of their finger glows with a bright yet not dazzling light. It is strong enough to turn night to day within 100m of the caster and across the length of a battlefield it will at least light up the area as if it were dusk, just about enough light to read by. The beacon also repels the undead, their strength being sapped by 7% per level of beacon while the light shines on them.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Guardian Light")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=3*60*60, cast_time=60)
data_list[-1].set_values(description="""A dull yet warm and comforting light shines from a few metres above the caster and reaches for 500m from the caster. All allies that it falls upon will have their armour strengthened by 10% per level and their resistance to mental based magic (illusions included) increased by 10%. At level 10 their armour will be twice as strong and they will be twice as resistant to mental attacks. The spell lasts for 1 hours and requires the concentration of the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Supernatural")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=20)
data_list[-1].set_values(description="""30 targets becomes infused with supernatural energy and power. Boosts of 8% per level are given to toughness, strength, agility, mental clarity, willpower and morale. The combined power of all these boost means they are very powerful even at level 1 of the spell. The spell lasts for 20 minutes but requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Scales of the Sun")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=20, tradable=False)
data_list[-1].set_values(description="""Up to 2 targets per level have their skin turned into brightly shining scales. Kinetic damage has no effect on them for 1 minute per level of the spell. Things such as fire and magical damage still harm them. Once cast the spell requires no concentration from the caster. Kinetic covers things such as falling, stabbing and hitting, it does not cover fire, electricity, ice or acid.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Prismatic beam")
data_list[-1].set_values(category=find_cat("Light"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=10*60, cast_time=1, tradable=False)
data_list[-1].set_values(description="""A narrow beam of light shines forth from the caster's hand with a radius of 0.1cm. It lasts for 10 seconds per level and will cut through metal and stone at a rate of 10cm a second. If moved at the right speed it can cut a hole in an object. The spell requires the concentration of the caster to maintain. Note that the beam has line of sight range but aiming it gets harder at longer ranges and you have but a narrow beam.

<div class="advanced">
	
</div>""")

#	DARK
#------------------------
data_list.append(Spell())
data_list[-1].set_values(name="Shapeshift")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=30*60, cast_time=300)
data_list[-1].set_values(description="""The caster turns themselves into a comparably sized creature of some kind. They cannot grow or shrink more than 30% of their real size nor will they take on magical properties of what they become, only physical ones. The spell lasts for up to 1 week per level after which it will revert. At level 10 the caster may use the spell on a willing or unconscious target instead of themselves if they wish. The caster may cause the spell to revert early if they wish. The spell is able to mimic specific features such as faces.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Transmute")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=30*60, cast_time=60)
data_list[-1].set_values(description="""A metal is transformed into a different (non-radioactive) type of metal. This is a touch spell and up to 2 litres (200<sup>3</sup>cm) per level of metal or stone may be transformed per casting. The spell lasts only 24 hours after which the metal will revert to it's original form.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Invisibility")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=10*60, cast_time=20)
data_list[-1].set_values(description="""The caster and personal objects they hold become invisible for the duration of the spell. They will shimmer slightly in intense light or underwater but even then are still very hard to spot. If they touch something or someone not invisible the invisibility will fade until they stop touching such an object (the exception being the floor). Upon casting the caster will slowly fade over the course of 11 seconds less 1 second per level. The spell lasts 60 seconds per level but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Read Mind")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=2*60, cast_time=5)
data_list[-1].set_values(description="""The caster sees into the mind of the target and can hear their current thoughts, if the target is aware of this at casting then they can deflect the spell if they have more willpower than the caster. If the target is aware or becomes aware of this then they can attempt to break the connection by summoning enough willpower and forcing the caster out. Each level gives the caster a 10% bonus to their willpower for such a conflict (but not the initial casting). The spell lasts for up to 1 minute per level and requires the concentration of the caster to maintain.

Read mind allows the caster to know everything that is passing directly through the conscious mind of the target, they cannot access memories and thoughts that are not conscious and current.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Create Image")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=5*60, cast_time=5)
data_list[-1].set_values(description="""An image is created, it has no physical properties except that it is visible. It is completely controlled by the caster and cannot be moved more than 50m away from them. The spell lasts for 2 minutes per level and requires the concentration of the caster. The image cannot be larger than 3m in any dimension.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Cripple")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=3)
data_list[-1].set_values(description="""A target within 100m is struck by crippling pain and weakness. They can barely stand, much less fight. Exceptionally strong or tough targets will find the effects lessened. The spell lasts for 60 seconds per level but requires the caster's full concentration to maintain.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Curse")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=2)
data_list[-1].set_values(description="""The target becomes cursed by bad luck, what should have just about hit a target will miss, what should have been a bullseye shot will be off to the side. The spell lasts for 5 minutes per level but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Mind blast")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=30, cast_time=2)
data_list[-1].set_values(description="""A focused blast of mental energy is thrown at the target. They can completely deflect the damage if they have more willpower than the caster but the more that the caster has than they do the more damage they will take. If the caster has enough then they can kill the target by simply blowing apart their mind. Each level gives a 15% willpower boost to the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Darkness")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=20*60, cast_time=10)
data_list[-1].set_values(description="""All light sources within 60m of the caster dim to a quarter of their normal amount, the suns rays in that area will dim to a tenth of their normal and the rays of the moon will be completely removed. The light is altered when it enters the area of the spell, not at the source. The spell lasts 5 minutes per level but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Collapse")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=60)
data_list[-1].set_values(description="""The caster places their hands onto a building and while the spell is in effect the foundations will slowly turn to sand as will the substances holding the building together. Normal buildings will fall after only minutes of this spell while walls and reinforced structures can take days. The spell lasts for 5 minutes per level and requires the full concentration of the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Mass suggestion")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=20*60, cast_time=60)
data_list[-1].set_values(description="""100 targets per level become much more susceptible to the words of the caster, those with more than half the willpower of the caster will not be affected and those that realise they are under the effects of the spell will cease to be affected by it. Each level also grants the caster a 20% willpower boost for the purpose of placing people under the effects of this spell. The spell lasts for an hour but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Control Mind")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=30*60, cast_time=10)
data_list[-1].set_values(description="""The target's mind is taken over by the caster, they see through the eyes of their target and force their willpower upon them. The caster is given a 20% boost to their willpower per level of the spell and if at any time the target manages to overpower the caster in terms of willpower the spell will be instantly broken. The spell lasts for as long as the caster can maintain the control (line of sight need not be maintained) though the caster will obviously be unable to do things with their own body while controlling the mind of another.

Weaker targets will be completely unable to fight the effects of the spell at high levels and if cast by a willful caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Telepathy")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=5*60, cast_time=5)
data_list[-1].set_values(description="""The caster links minds with the target allowing them to speak thoughts to each other. The target can break off the connection at any time. The spell lasts 60 seconds per level and requires the caster's concentration to maintain.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Doom")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=20*60, cast_time=3)
data_list[-1].set_values(description="""Up to 3 targets become doomed, all damage dealt to them will increased by 30% per level of the spell and their location will be known to the caster as long as the spell remains. The spell lasts for 1 day per level of the spell but requires no concentration. The spell has a range of 100m.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Puppet Master")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=10)
data_list[-1].set_values(description="""The target has a small mental splinter placed in their mind. The caster can whisper thoughts into the mind of their target and over time can make them do what they want. The spell lasts for 5 weeks per level of the spell but requires no concentration to maintain.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Split Mind")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=300)
data_list[-1].set_values(description="""The caster places a portion of their mind into the mind of a willing target. From here they can communicate instantly with the target via thought. The spell allows 1 target per level though each casting only targets one mind at a time. If a carrier of any of the splits is killed then the caster will fall unconscious for 12 hours, if another is killed in this time then the caster will die. Splits can only be removed by the caster and require touch. The spell lasts until removal or death but requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Morph Land")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=60)
data_list[-1].set_values(description="""The land within 10m of the caster per level slowly moulds itself to the caster's will. Earth moves very slowly, 1 metre over the course of 24 hours. Using this spell it is however possible to create very interesting terrain. The spell lasts for 1 hour and requires the caster's full concentration to maintain.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Ghost army")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=5*24*60*60, cast_time=60, tradable=False)
data_list[-1].set_values(description="""A force of up to 2500 men per level of the spell is created. It can take the form of any force that the caster imagines and move as far from the caster as wished. The illusion cannot move faster than the speed of a galloping horse. It will kick dust into the air and appear to be completely real until touched at which point the physical object will simply move through it. The caster has a large amount of control over the illusion and can cause parts of it to die as needed.

The spell requires the caster's concentration to control but when not being directly controlled requires no concentration. It will last up to 5 days.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Simulacrum")
data_list[-1].set_values(category=find_cat("Dark"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=30*60, cast_time=1, tradable=False)
data_list[-1].set_values(description="""1 Simulacrum is created per level, each is a perfect replica of the caster and any changes to the caster's physical appearance will instantly appear on all simulacrums. Each Simulacrum is completely insubstantial and cannot move further than 300m away from the caster. The caster is able to instantly swap positions between himself and any of the simulacrums and the change will not be apparent. Simulacrums can be destroyed by striking them with a physical object. The spell requires no concentration from the caster and will last up to 10 minutes. The caster cannot see through the simulacrums.

<div class="advanced">
	
</div>""")

#	DESTRUCTION
#------------------------
data_list.append(Spell())
data_list[-1].set_values(name="Whirlwind Of Fire")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1*60, cast_time=5)
data_list[-1].set_values(description="""The air around the caster begins to spin and heat up, when the spell casts the air ignites and expands outwards up to 5m away. Those struck will often be set aflame or at least suffer serious burns. The air around the caster is not affected so the caster will not suffocate. The spell lasts for 1 second per level of the spell but requires no concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Incinerate")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1*60, cast_time=2)
data_list[-1].set_values(description="""A target within 40m is set on fire. If they are wearing nothing flammable then they will often survive withonly minor injuries. The fire lasts for a minimum of 0.5 seconds per level of the spell but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Fireball")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=20, cast_time=1)
data_list[-1].set_values(description="""A ball of liquid fire is blasted out from the caster's hand. It is affected by gravity but is very light so makes for poor artillery. Upon impact or after 100m the fireball will explode and spray burning fire over a 0.5m radius. Each level upgrade drops cooldown by 1.5 seconds, at level 10 it will have a cooldown of 6.5 seconds.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Push")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=15, cast_time=1)
data_list[-1].set_values(description="""The target is thrown backwards, an unarmoured human will fly back at 5mps while a man in full plate more like 2-3. The spell lasts 1 second per level and requires the concentration of the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Lightning Bolt")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=50, cast_time=4)
data_list[-1].set_values(description="""A bolt of lightning strikes the area within 50m of the caster. The spell is quite capable of striking allies and will be attracted to something to ground it, a tree, a metal clad soldier. The spell will not cast if there are not clouds from which to bring down lightning. The cooldown falls by 4 seconds each upgrade, at level 10 it will have a cooldown of 14 seconds.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Firebang")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1.5*60, cast_time=1)
data_list[-1].set_values(description="""A small ball of fiery energy flies from the caster's hand on a flat trajectory. After either traveling 50m or striking an object it will explode and send small globules of fire everywhere. These burn out after 1 second per level but travel about 50m each.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Shattering blow")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=5, cast_time=1)
data_list[-1].set_values(description="""The next physical strike that the caster makes will impact with 100% more force per level of the spell. Note that if you swing a hammer with enough force onto something tough enough you will shatter your hammer.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Decay")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1*60, cast_time=10)
data_list[-1].set_values(description="""The target must be completely inanimate, while this spell is affecting something the ravages of time will happen far faster. The object will age 1 year every second per level of the spell. The spell is unable to affect anything larger than a human. The spell lasts for 10 seconds and requires the concentration of the caster.

<div class="advanced">
	 - Animated constructs cannot be buffed or cursed by other spells
	 - Should the construct recieve large amounts of structural damange then it will become disenchanted
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Heatwave")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=60)
data_list[-1].set_values(description="""The air around the caster heats up to a degree above what it should be per level of the spell. This air will move via convection currents and over time heat up the air in a much larger area, especially with multiple casters. The caster themselves is unaffected by this heat. The spell lasts for as long as the caster keeps it going, it requires concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Lava Flow")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=2*60*60, cast_time=60)
data_list[-1].set_values(description="""The rocks 10m below the caster heat up massively and rise to the surface as magma whereupon it will burst from the ground as lava, typically this takes 5-10 minutes. The spell affects Rocks a cylinder of rocks 1m below the target point with a radius of 0.5m per level. As long as the spell is maintained the rocks will heat up, the spell requires the caster's full concentration and also that their feet remain on the ground.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Pyromantic Blast")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=10)
data_list[-1].set_values(description="""A blast of energy strikes a point up to 100m away and explodes with severe force. Those within 10m of the blast will probably die while those between 10m and 30m will probably escape with severe wounds, those 30m to 50m away will probably be thrown to the floor. Each level increases it's power by 10%.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Disintegrate")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=30*60, cast_time=10)
data_list[-1].set_values(description="""An inanimate target object is turned to dust. The object may be up to 1 litre in volume per level.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Firestorm")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=60)
data_list[-1].set_values(description="""A burning rock falls from the sky and strikes a target point up to 100m away. The rock is 10kg per level of the spell and upon impact will probably explode and send fragments of very hot and burning rock over a large area. The rock takes 15 seconds minus one second per level to hit the ground and requires the caster's full concentration. If the spell ends early then the rock explodes before striking the ground and the caster suffers a miscast.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Wall Of Fire")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=30*60, cast_time=20)
data_list[-1].set_values(description="""A wall of fire 1m thick and 8m high is create between two points up to 20m apart per level. Neither point may be more than 150m away from the caster. The spell lasts as long as the caster maintains it, the spell requires concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Blizzard")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=60)
data_list[-1].set_values(description="""The air becomes chilled and begins to snow, given long enough a gale will blow and hailstones will fall from the sky. The spell affects an area of 1km around the caster and each level of the spell increases the power of the spell by 15%. The caster is completely immune to the blizzard. The spell lasts for an hour and requires the full concentration of the caster, multiple castings in one area will stack with diminishing returns. As a weather spell it will have reduced effect in areas that do not have the right conditions, deserts for example.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Earthquake")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=300)
data_list[-1].set_values(description="""The ground beneath the caster shakes and rumbles, if the spell remains uninterrupted then all the rock within 100m of the caster per level (flat horizontal plane) yet 1km below the caster will shift across several metres. The result is that everything above it will suffer from a strong earthquake. Alone it won't cause massive loss of life but it can rip apart city walls. The spell must be maintained for 6 hours and requires the caster's full attention and his feet must remain on the ground. During that time the area will rumble slightly though this will not affect the caster. The spell will be set off 30 minutes after the spell ends.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Control Weather")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=10)
data_list[-1].set_values(description="""The caster takes control of the weather within 500m per level of the spell. They can alter the pressure levels and wind patterns to form whatever weather they wish though will find it hard to create rainstorms in the desert or heatwaves on the poles. The spell lasts for only 5 minutes but the effects of what the caster puts into motion can last for up to a week, especially if reinforced. This spell requires the full concentration of the caster. Note that due to the duration of the spell it can be undone very easily but the actual reaches of this spell if used carefully can be large enough to affect several nations at once.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Hurricane")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=12*60*60, cast_time=300, tradable=False)
data_list[-1].set_values(description="""Strong winds blow from behind the caster in an area 1km around him per level. They make fighting into the wind impossible and even fighting with the wind at your back is hard. After the spell has been active for 5 minutes it will begin to rain. The spell lasts for 1 hour and requires the caster's full concentration. As a weather spell it will have reduced effect in areas that do not have the right conditions, deserts for example.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Forever burning")
data_list[-1].set_values(category=find_cat("Destruction"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=30*60, cast_time=10, tradable=False)
data_list[-1].set_values(description="""As long as the spell is in effect the target will burn with an intense flame that will melt iron in about 20 seconds. The spell requires the concentration of the caster and will last for up to 30 seconds per level. The target must be alive at the casting of the spell. The spell has a range of 50m.

<div class="advanced">
	
</div>""")

#	ABJURATION
#------------------------
data_list.append(Spell())
data_list[-1].set_values(name="Counterspell")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=10, cast_time=1)
data_list[-1].set_values(description="""A target spell that is still being cast or is being maintained is cancelled. The full cooldown of the spell is still applied and even increased by 10% per level of Couterspell.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Resistance")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=10)
data_list[-1].set_values(description="""The mental resistance of the target is increase by 35% per level. The spell lasts for 24 hours but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="See magic")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=5*60, cast_time=10)
data_list[-1].set_values(description="""The caster gains the ability to see magic up to 10m away per level of the spell. This means that they can see magical items, mages, spells currently in effect or people under the effect of spells. The more magic a spell uses the more visible it will be (puppet master is very hard to detect). The spell lasts for 60 minutes but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Disenchant")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=10*60, cast_time=2)
data_list[-1].set_values(description="""A target object within 3m per level has all magical enchantments removed from it. The spell takes 10 seconds to perform and during that time requires the caster's full attention.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Mana Burn")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1*60, cast_time=3)
data_list[-1].set_values(description="""All loose mana within 5m of the caster per level ignites instantly. Loose mana is caused by enchantments that have recharged and are awaiting use or mages casting spells. Those affected by the spells are not a source of loose mana. The caster is not affected by this spell.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Wall Shield")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=5)
data_list[-1].set_values(description="""The caster creates a bubble up to 1m in radius per level of the spell. The bubble is centred on the caster and will move with them. The bubble is completely impervious to the transfer of magical energy and any spells cast from out to in or in to out will instantly cease. The shield will absorb magical energy as long as the caster maintains it. The shield requires the caster's concentration.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Disruption")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=5)
data_list[-1].set_values(description="""A target within 50m has their ability to cast spells disrupted. Their chance to miscast is increased by 20% per level of Disruption, additionally the cooldown of all their spells is increased by 10% per level of disruption. The spell lasts for up to an hour but requires the concentration of the caster. Note that this is a a % alteration to the current miscast chance, if they have a 20% miscast chance then level 5 will turn that into 40%.

<div class="advanced">
	This does not affect the strength of a daemonic being, their base miscast value is used for that.
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Prepare spell")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0)
data_list[-1].set_values(description="""This is not an actual spell, it alters the next spell to be cast. The cast time of the next spell becomes double what it normally is but the cooldown is lowered by 5% per level of Prepare spell.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Focus spell")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0)
data_list[-1].set_values(description="""This is not an actual spell, it alters the next spell to be cast. The cast time of the next spell is tripled but the power or effect of the spell is increased by 5% per level of focus spell.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Sanctuary")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=30*60, cast_time=10)
data_list[-1].set_values(description="""The area within 5m of the caster per level becomes untouchable by summoned creatures, they cannot enter it. Summoned creatures that do enter it will lose any sustaining power from their caster, this means that a creature that is summoned yet not sustained will not be affected by the spell. The spell requires the caster's full attention.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Dispel")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=20*60, cast_time=20)
data_list[-1].set_values(description="""All enchantments within 100m of the caster take 20% longer to recharge per level of the spell. The spell lasts for an hour and requires the concentration of the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Absorb shield")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=40*60, cast_time=15)
data_list[-1].set_values(description="""Identical to the wall shield but instead of simply "stopping" magic it absorbs only inbound spells, spells fired from inside are unaffected. As a spell leaves the shield it will leave a hole in the shield that will take a few seconds to close, this can be fired through by those outside of the shield.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Telekinesis")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=5*60, cast_time=5)
data_list[-1].set_values(description="""The caster creates a copy of their hand made from energy. It is visible but creates little light, it is as strong as a human hand but with a 20% strength increase per level of the spell. It is under the control of the caster and can move at 2mps. The spell lasts for up to 20 minutes and requires the caster's concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Mana drain")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=15*60, cast_time=3)
data_list[-1].set_values(description="""The target finds the power of all their spells falls by 6% per level of Mana drain. The spell lasts as long as the caster maintains it, it requires their concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Control Time")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=1)
data_list[-1].set_values(description="""A 1m raidus per level of the spell bubble appears at a point up to 50m away. Everything inside it experiences time at a rate 8% slower than normal. The bubble is stationary, visible and forms over the course of 2 seconds. The spell lasts as long as the caster maintains it and it requires their full concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Control Gravity")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=5)
data_list[-1].set_values(description="""The area 4m around the caster per level of the spell experiences either double the normal gravity or half the normal gravity, caster excluded. The gravity amount is chosen upon casting the spell and will remain as long as the caster maintains the spell, this requires their full concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Null magic field")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=3*60*60, cast_time=60)
data_list[-1].set_values(description="""The area 10m around the caster per level of the spell becomes a null magic field. No spells can be cast from within it and all magical items energy drains away in moments. Magical entities find their energy sapped from them with alarming speed. The area remains fixed and will last for 60 minutes and is in no way connected to the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Fountain of Mana")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=30, tradable=False)
data_list[-1].set_values(description="""All non-master tier spells cast within 50m of the caster have their cooldown lowered based on the tier of the spell in question. Low tier spells reduce at 9% per level of Fountain, Mid at 7% and High at 5%. This also applies to items and enemies of the caster. The spell lasts for up to 24 hours and requires the full concentration of the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Time lapse")
data_list[-1].set_values(category=find_cat("Abjuration"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=30*60, cast_time=0, tradable=False)
data_list[-1].set_values(description="""The caster instantly reappears exactly as they were up to 6 minutes ago per level of the spell. Their location, health, stamina and physical well-being are exactly as they were at that point in time. Spell cooldowns are not affected. If the caster would reappear in the same location as another physical object they can adjust the time so that they do not. This is not a time traveling spell.

<div class="advanced">
	
</div>""")

#	DAEMONIC
#------------------------
data_list.append(Spell())
data_list[-1].set_values(name="Transfigure")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=2*24*60*60, cast_time=300)
data_list[-1].set_values(description="""The caster turns themselves into a Daemonic entity. They grow 5% larger per level and additionally gain a 20% boost per level to their strength and agility. Transfigure requires the souls of 5000 people that died violently within the last 24 hours in one area or the soul of a single special being (such as a chosen) in the last year, the latter method is unable to use allied souls. Once you cast this on yourself you can no longer possess yourself. For more information, see the <a href="progression.php">daemonic progression</a> rules.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Banish")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=1)
data_list[-1].set_values(description="""A target being from another world within 100m is blasted with energy. Banish causes a weakening of the ties that being has to this world. In daemonic terms banish reduces the control range by 0.2m per level. If a daemon is cut lose from it's controllers with banish then it will become neutral rather than aggressive specifically towards it's captors, it will become most aggressive towards other daemons. Repeat castings will further weaken the being until it returns to it's home.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Translocate")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=60, cast_time=0)
data_list[-1].set_values(description="""The caster transports themselves through the planar dimensions and reappears up to 5m away. The spell makes a distinctive noise and takes 1 second to actually move them during which time they will exist in another plane of existence. Upgrading this spell reduces cooldown by 6 seconds per level, at level 10 it's cooldown will be 6 seconds.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Elgr")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=600)
data_list[-1].set_values(description="""Elgr look like palid and famished humans, their sagging skin giving them quite a haunted appearance. They are half as strong as a human and cannot move very fast. They can however walk through walls, they move at 10% of their normal rate per level of the spell. Elgr require 1 mage to control them and must remain within 1000m of their summoner or control will be lost.

Those possessed by the Elgr lose half of their strength and half of their agility but can walk through walls at 10% of their normal speed per level of the spell.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Red widow")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*24*60*60, cast_time=600)
data_list[-1].set_values(description="""The Red widow is one of the smartest and most cunning daemons. It takes the form of a seductive female and is an expert at seduction. It can however transform in seconds into a giant spider-creature with legs that can skewer it's often unarmoured targets. Each level boost the intelligence of the Red widow by 50%, with such a boost comes a higher cost in willpower. Red widows require only a single mage to control them and can venture up to 4000m away from their controller before control is lost.

Those possessed of a Red widow gain only a 10% boost to their charisma per level of the spell. The Red widow is not strong in the form of possession and one of the safest daemons to be possessed by.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Gragar")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1*24*60*60, cast_time=600)
data_list[-1].set_values(description="""Gragar are hulking brutes, they're humanoid but stand 2m tall and possess large wings. They are capable fliers and with each level they become 15% stronger meaning they can fly faster and rip more bones from bodies faster. Gragar are simple daemons. Gragar require 1 mage to control them but must remain within 750m of their summoner.

Those possessed by the Gragar grow giant wings and gain a 10% strength boost per level. They will however tire four times faster and the Gragar grow stronger while their host sleeps, many hosts will not survive more than a few days.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Screamer")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=1*24*60*60, cast_time=600)
data_list[-1].set_values(description="""Screamers are humanlike except that they have 6 arms and are amazingly muscled. Each arm ends in a metal blade as if it were placed inside them unnaturally. They are completely insane and very hard to direct correctly, they are fast runners and twice as strong as a human, each level of the spell gives them a 10% boost to their strength. Screamers require 4 mages to control and must remain within 2000m of all the summoners or control will be lost.

Those possessed by a screamer gain a 100% boost to their agility and then also a 20% boost to their strength per level of the spell. However with every kill they slip slightly closer to insanity until they are the same as the Screamer.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Shifter")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=12*24*60*60, cast_time=600)
data_list[-1].set_values(description="""Shifters can take on the appearance of any race they choose though cannot grow or shrink more than 40%. They can extend a sharp talon from the back of their hand and strike with enough force to puncture even full plate. Their main role is to infiltrate an army and slay officers within it, often mimicking the appearance of those it has killed. Each level provides a 20% boost to it's ability to trick and beguile it's opponents. Shifters require 1 mages to control them. Shifters can venture great distances from their summoners, control is instead lost through time, a shifter will last for 1 month before control is lost and the shifter will break free of the spell. If the shifter is more than 4000m away from their summoner then the rate of loss is doubled and if they are more than 1km from the mage then it will be multiplied by 10.

Those possessed by a Shifter gain it's ability to change shape rapidly but with each kill the Shifter moves closer to taking control of their mind. Each level of the spell grants a 15% charisma boost to the possessed.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Metamorphose")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=7*24*60*60, cast_time=20*60)
data_list[-1].set_values(description="""The caster must already be transfigured to perform this and cannot metamorphose to a higher level than they can transfigure. Metamorphosed grow 5% larger per level of the spell and have their toughness and maximum health increased by 5% per level of the spell. Additionally they gain a 50% increased rate of regeneration of health and stamina. Metamorphosis brings with it small wings useful for falling from great heights. Metamorphose requires the souls of 35,000 people that died violently within the last 24 hours in one area or the souls of 4 special beings that died within the last year (first ones count for 3 souls). The latter method cannot use allied souls. For more information, see the <a href="progression.php">daemonic progression</a> rules.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Plane Jump")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=10*60, cast_time=10)
data_list[-1].set_values(description="""4 targets per level of the spell are moved to a different world. They will be disorientated for a few seconds but there are no serious or long lasting effects. If cast on an enemy then it's range falls to 4m per level.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Implode")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=20*60, cast_time=6)
data_list[-1].set_values(description="""A target inanimate object up to 50m away of up to 1 litre volume per level is compressed to a quarter it's size and the energy released. If the object was dense it will probably explode, tougher objects throw out better shrapnel. The spell takes 10 seconds to complete and in this time requires a caster's full concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Tesauro")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=7*24*60*60, cast_time=1200)
data_list[-1].set_values(description="""Tesauro weaken the link of daemons to those that control them, all opposing daemons within 100m of the Tesauro count as being 10% further away from their summoner(s). The effect stacks at an additional 1% per level per Tesauro. Tesauro have the physical apperance and strength of a young human child (pre-teen), they are also easily spotted as their aura is noticable even to those not versed in magic. Tesauro require 16 mages to control them (8 mid tier mages) and must remain within 500m of their summoners or they'll break free.

Due to their nature Tesauro cannot be used for possession.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Gymander")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=3*24*60*60, cast_time=1200)
data_list[-1].set_values(description="""Gymanders are humanoid and dress in flayed human skin. They fight with long cutting knives and weild them with amazing accuracy and speed. They leave their victims writhing on the floor in agony and feed off of the pain, each wailing victim gives them a small boost to their toughness and speeds regeneration of health. Each level increases the speed of the Gymander by 15%. Gymanders require 8 mages to control them (4 mid tier mages), they can venture up to 2000m away from their summoners before they break free.

Those possessed by a Gymander will be weakened massively, their strength and toughness will halve but their will feed from those they cause pain to. This effect is improved 20% per level of the spell.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Infernal")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=4*24*60*60, cast_time=1200)
data_list[-1].set_values(description="""Infernals are twice the height of a human and built from rocks. They are awash in a green flame and though cumbersome are very strong. They are vulnerable to water as rapid cooling causes them to shatter, they are brittle and heavy hand weapons can also bring them down. If however you are bereft of such things your best bet is to flee. Each level increases the strength of the Infernal by 20%. Infernals require 8 mages to control (4 mid tier mages). Infernals can travel up to 4000m away from their summoners before breaking free.

Those possessed by an Infernal have their agility reduced to a third of what it was but change to resemble the Infernal and have their strength increased by 30% per level of the spell.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Gate")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=3*60*60, cast_time=10*60)
data_list[-1].set_values(description="""A giant circular portal 3m in radius is created before the caster. This gate may go to any of the other worlds and will last as long as the caster maintains it, this requires their full concentration. When the spell ends the caster is also taken through the portal as it closes. The portal will always come out in the exact same location on the other world, those traveling through will find themselves weak and in need of rest, mages will be in a state as if they just cast a spell with a 3 hour cooldown. These effects are lowered by 10% per level of gate.

<div class="advanced">
	While the gate is forming it will be visible on the target world.
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Ascension")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=4*7*24*60*60, cast_time=40*60)
data_list[-1].set_values(description="""The caster must already be metamorphosed to perform this and cannot ascend to a higher level than they can metamorphose. Ascended can cast plane jump to Enkhingi at any location on the world and physically grow 10% bigger per level of Ascension. Ascended daemons also gain a 5% resistance to all spells per level, things such as fireball will hurt just as much but purely magical effects such as Doom will have their effects lowered in power.

In addition the short stubby wings grow large enough for full flight, when fighting with their bare hands they deal daemonic damage which can have more of an effect on first ones, daemons and some other special beings (not Chosen or most First ones). Ascension requires the souls of 100,000 people that died violently within the last 24 hours in one area or the souls of 8 special beings that died within the last year. The latter method cannot use allied souls. For more information, see the <a href="progression.php">daemonic progression</a> rules.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Loki")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=31*24*60*60, cast_time=30*60)
data_list[-1].set_values(description="""The Loki is angelic in appearance, glowing with inner power and standing 3m tall. It is strong enough to take down an elephant with it's bare hands yet carries a massive greatsword. They posses strong wings and are capable fliers. Loki require 12 mages (3 high tier) to control them, this allows them to travel up to 500m away from their summoners. Every mage point added to the pool increases this distance by 100m (so an extra 300m per high tier mage), the downside is that anybody magically talented can easily trace the lines of power from the Loki back to it's summoners, cutting them down can quickly cause it to break free.

Each level of the spell grants the Loki 15% more strength.

Loki cannot be used for possession.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Cyrgai")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=120, tradable=False)
data_list[-1].set_values(description="""A squad of Cyrgai daemons are summoned to serve the caster, cannot be unsummoned or banished. Each one has a WP of 0.1, as many can be summoned as wanted. They will remain around the caster to protect them. Cyrgai willpower does not change with the presence of other daemons. Cyrgai are equipped with a small shield and a spear. They look like humans but are twice as strong, agile and tough as humans. Additionally they fight without tire, without fear and with great group coordination. Cyrgai become 10% larger per level.

Unlike other daemons the Cyrgai are semi-loyal to their summoner and while the summoner sleeps naturally they will protect them rather than requiring willpowered control. Cyrgai must remain within 50m of their summoner or they will unsummon.

<div class="advanced">
	
</div>""")

data_list.append(Spell())
data_list[-1].set_values(name="Demigod")
data_list[-1].set_values(category=find_cat("Daemonic"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=6*31*24*60*60, cast_time=60*60, tradable=False)
data_list[-1].set_values(description="""The caster must already be ascended to perform this and cannot use this spell at a higher level than they are ascended to. Demigods radiate power and their presence will be noticeable to all within 100m, the energy field of the daemon will extend to cover any melee weapon they use. Demigods grow 10% larger per level of Demigod. The hide/skin of the daemon becomes 20% tougher against physical attacks per level of demigod. The wings of the daemon also double in strength meaning that they can fly even in bad weather.

Demigod requires the souls of 320,000 people that died violently within the last 24 hours in one area or the souls of 16 special beings that died within the last year (first ones count for 3 souls), the latter method cannot use allied souls. For more information, see the <a href="progression.php">daemonic progression</a> rules.

<div class="advanced">
	
</div>""")


#	NECROMANCY
#------------------------
data_list.append(Spell())
data_list[-1].set_values(name="Freeze")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=2*60, cast_time=2)
data_list[-1].set_values(description="""The tip of the caster's finger becomes very very cold (100 kelvin, -173 C or -279 F). The spell prevents the caster from being affected but anything that they touch will be chilled. The spell lasts for 1 minute per level and requires the concentration of the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Flesh To Stone")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=4*60, cast_time=10)
data_list[-1].set_values(description="""The target is turned to stone or if already affected by this spell, turned back into living form. Each level increases the toughness of the stone, at level one it will shatter from a strong hammer blow, at level 10 it is laced with metal and nearly shatterproof. The spell requires touch to work and takes 10 seconds to work during which the full concentration of the caster is required. If cast upon oneself then the spell will reverse after 60 seconds, taking 10 seconds to do so.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Heal")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=5*60, cast_time=4)
data_list[-1].set_values(description="""The lifeforce of the target is completely restored. Any illness, tiredness, loss of blood or broken bone is mended. Wounds that would have taken months or even years to heal are healed by the spell. The spell requires the caster to be touching the target and takes 10 seconds to work and taking the full concentration of the caster during this time. Each level reduces the spells cooldown by 30 seconds, at level 10 the cooldown is 30 seconds.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Skeletons")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=20*60, cast_time=120)
data_list[-1].set_values(description="""
10 skeletons per level are drawn from the ground, during the casting time they claw their way to the surface and gather around the caster. The spell lasts as long as it can be maintained but requires the full concentration of the caster to maintain. The skeletons must remain within 400m of the caster. Skeletons are armed with a crude axe and buckler.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Zombies")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=20*60, cast_time=120)
data_list[-1].set_values(description="""Identical to the summoning of skeletons except that zombies are summoned instead. Zombies are far tougher than skeletons but cannot use weapons.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Regeneration")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=6*60, cast_time=10)
data_list[-1].set_values(description="""One target per level regrows lost limbs and recovers from all natural ailments over the course of this spell. The spell lasts for 3 hours and by the end of it all lost limbs and disfigurements will have been recovered. If cast on a healthy person then it will still last 3 hours but instead rapidly speed the recovery of stamina to the extent that they can exert themselves fully over those 3 hours needing only to take very short rests.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Vampyric touch")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=3*60, cast_time=2)
data_list[-1].set_values(description="""The caster drains from their target all life energy. Spells upon the target take 2 seconds each to destroy, once they are gone the lifeforce of the target begins to be sapped. Targets will fall unconscious within moments and even chosen will succumb to it's effects within 2 seconds. The caster is not limited to one target, after finishing with one they may move onto the next. The spell lasts 10 seconds per level but requires no concentration.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Corrupt flesh")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=4*60, cast_time=10)
data_list[-1].set_values(description="""The target's flesh corrupts and they become amazingly strong, 100% stronger per level of the spell. They are so strong that they can smash apart their own bodies, especially at higher levels. After the spell ends they will be so weak they cannot even walk for six hours, chosen often recover faster. If casting on an opponent the spell has a range of 50m. The spell lasts for 1 hour and requires no concentration.

<div class="advanced">
	
</div>""")



data_list.append(Spell())
data_list[-1].set_values(name="Sazulu")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=10*60, cast_time=1)
data_list[-1].set_values(description="""A blast of Necromantic energy strikes a target within 100m. The blast will kill any common human instantly and severely weaken something stronger. If the target dies from the spell then they will explode, a human will explode with a radius of 15m while something like an elephant with 50m. Each level of the spell increases the power of the blast by 10%. After being struck by this spell you will be immune to it for 1 hour minus 4 minutes per level of the blast you were hit with.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Restoration")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=10*60, cast_time=20)
data_list[-1].set_values(description="""4 targets per level are restored as if they'd just had a good night sleep. Minor injuries are healed, stamina replenished, morale boosted and generally a soldier that was on their last legs will be as good as a fresh one. Repeated use of this spell without sleep will bring about exhaustion as it does not completely rejuvinate the mind and body.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Healing pulse")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=15*60, cast_time=30)
data_list[-1].set_values(description="""All allies within 30m per level receive a small healing boost, this also replenishes some stamina too. Targets can be taken to up to 3% per level above normal health maximums, many castings of this can create an undying army.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Affliction")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=30*60, cast_time=10)
data_list[-1].set_values(description="""The target begins to feel weak, they lose 25% of their strength and stamina and if they die while the spell is in effect, all enemies of the original caster within 5m will become infected with a new copy of the spell. The spell lasts for 30 seconds per level and requires no concentration from the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Imbue spirit")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=6*60*60, cast_time=60*30, range=20)
data_list[-1].set_values(description="""A weak necromantic spirit inhabits an inanimate object and brings it to life. The spirit can only exert force from inside the object and at one point at a time only; it can exert 1kg (9.8 newtons) of force per level. The spirit will tire quickly and has energy for up to 1 hour of exertion, it takes 4 hours to recharge fully when empty. Each object can have only 1 spirit inside them at a time though a larger object can be made of many objects that work in combination under the command of their animator. Spirits only function under the command of the caster and only while within 1km of that caster.

<div class="advanced">
	 - Animated constructs cannot be buffed or cursed by other spells
	 - Should the construct recieve large amounts of structural damange then it will become disenchanted
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Bibgri")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=1*60*60, cast_time=240)
data_list[-1].set_values(description="""Identical to the summoning of skeletons and zombies except that bibgri are summoned. Bibgri are similar in appearance to zombies but are twice as strong as a man and move nearly as fast. They don't use weapons but are very tough and strong. Bibgri may go as far as 600m from the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Resurrection")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=24*60*60, cast_time=300)
data_list[-1].set_values(description="""4 target bodies per level are restored to life by the spell. They will be healed instantly and awake as if they had merely been sleeping. The bodies may not have been dead any longer than 48 hours or the spell will not work. If a chosen one dies and is not brought back within 48 hours then this spell may still bring them back at any time and create a new body for them to use. They will be be asleep for 60 days minus 5 days per level of this spell, at the end of which they will awake.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Terralan")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=12*60*60, cast_time=300)
data_list[-1].set_values(description="""A single Terralan is summoned from the ground before the caster. Terralans are 2m tall and built from whatever they came from. Stone creates armour, plants create a regenerating monster while sand will create something that is simply immune to small weapons as it's made from sand. Terralans are 150% stronger and tougher than a human per level of the spell. The caster may choose to create the Terralan around them, trapping themselves within it's heart, while like this they can be moved without breaking their concentration. The spell requires the full concentration of the caster and the Terralan cannot go further than 150m from the caster.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Hordlings")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=12*60*60, cast_time=300)
data_list[-1].set_values(description="""10 skeletons are summoned per level of the spell, when they die they still remain alive and will try to put themselves back together. The result is a horde that must often be killed several times before it will stay down. The hordlings are unable to venture further than 600m from the caster and the spell requires the caster's full concentration to maintain.

<div class="advanced">
	
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Animate")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=24*60*60*30, cast_time=60*30, tradable=0, range=20)
data_list[-1].set_values(description="""An inanimate object is animated with the power of life. Objects smaller than a child cannot be animated nor can those larger than an elephant. The item can move up to 100kg per level plus 10% of the weight of the object per level. The result of that is that a big object has less strength left over for lifting but in total has more strength and would beat a smaller animation in a contest of strength. The spell lasts for 30 days. Joints and moving parts will automatically be created by the spell based on the shape of the object.

[pos]Speed wise an animated object the size of a human will generally be about 20-50% faster than a human. Upping the size of an animation will not reduce the speed of the object and when combined with a larger step distance will actually mean it can move faster. Animations have a slight lag to their reflexes of about a tenth of a second which makes them poor swordsmen against skilled opponents but brings little disadvantage against larger opponents.

<div class="advanced">
	 - Animated constructs cannot be buffed or cursed by other spells
	 - Should the construct recieve large amounts of structural damange then it will become disenchanted
</div>""")


data_list.append(Spell())
data_list[-1].set_values(name="Undying")
data_list[-1].set_values(category=find_cat("Necromancy"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=30*60, cast_time=5, tradable=False)
data_list[-1].set_values(description="""For 1 minute per level you are unkillable. You can be sliced in half but can still control both halves and feel no pain from the damage. When the spell ends you are once again able to feel pain and die. If during this time you "die" and get healed up you will remain alive after the spell ends.

<div class="advanced">
	
</div>""")


#	ALCHEMY
#------------------------
# http://woarl.com/board/viewtopic.php?f=101&t=2331
data_list.append(Spell())
data_list[-1].set_values(name="Mercury")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Also known as quicksilver, mercury is a grey metal that is found as a liquid when at room temperature.""")

data_list.append(Spell())
data_list[-1].set_values(name="Lead")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Lead is a dense, silvery-grey metal, that is mildly poisonous. Many alchemists spend their lives attempting to turn it, and other base metals, into gold.""")

data_list.append(Spell())
data_list[-1].set_values(name="Sulphur")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""In an unaltered state Sulphur occurs in a yellow crystalline form, and can be found near to volcanoes. It is also known as Brimstone.""")

data_list.append(Spell())
data_list[-1].set_values(name="Lime")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Lime is a simple inorganic reagent, that often appears as a white powder.""")

data_list.append(Spell())
data_list[-1].set_values(name="Potash")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Potash is a form of salt, created by leaching wood ashes and evaporating the solution formed.""")


data_list.append(Spell())
data_list[-1].set_values(name="Firesand")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Firesand resembles normal sand, albeit of a very pale colour. It is found in a few deposits across the world, and is quite resistant to the conduction of heat. Some desert peoples have been known to line heavy armour with it, so as to keep the individual cool within.""")

data_list.append(Spell())
data_list[-1].set_values(name="Bottled Lightning")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Though many alchemists know of bottled Lightning and its creation, there is an unwritten code that keeps it a secret from the masses. Usually held in glass, it resembles a pale blue liquid with a similar thickness to water.""")

data_list.append(Spell())
data_list[-1].set_values(name="Blessed Earth")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Taken from temples and chapels the world over, Blessed Earth is believed to imbue a small spark of divinity into the simplest of potions, and is thus used by many alchemists. There is some dispute as to differences caused by soil blessed by different gods and ascendants, but no outstanding evidence that has proved or disproved either side in such a debate.""")

data_list.append(Spell())
data_list[-1].set_values(name="White Acid")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""This strong acid is often confused with milk, and has led to several deaths as alchemists' children get themselves a drink while unsupervised.""")


data_list.append(Spell())
data_list[-1].set_values(name="Kdarkk")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Kdarkk is a rare plant known to grow in the coldest of conditions; it has been found around the polar icecaps, as well as high up mountain ranges.""")

data_list.append(Spell())
data_list[-1].set_values(name="Diamond Dust")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""This reagent is actually composed of thousands of microscopic diamonds, and is not to be confused with the clouds of ice known by the same name. The technology required to crush diamonds to create this dust is rare and expensive, and so known by few and used by fewer.""")


data_list.append(Spell())
data_list[-1].set_values(name="Primal Stone")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""Primal Stone is rumoured to be the first pieces of the many worlds Arl created, and is known only in a few small deposits, the majority of the rock having been reworked through volcanism. It is almost always dark, hard, and igneous, and is rarely found in pristine condition, having been subject to years of weathering and erosion.""")

data_list.append(Spell())
data_list[-1].set_values(name="Dragon's Blood")
data_list[-1].set_values(category=find_cat("Alchemy"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=15)
data_list[-1].set_values(description="""This reagent is not particularly accurately named; it is not necessarily blood, with many other organic humours also fitting into the category, and neither does it have to be from a dragon, with drakes, hydras, kraken and other almost mythical creatures dying for its production.""")


#	ENCHANTMENTS
#------------------------
data_list.append(Spell())
data_list[-1].set_values(name="Tank enchantment (Low)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Healer enchantment (Low)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Mage enchantment (Low)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Rogue enchantment (Low)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Low"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")


data_list.append(Spell())
data_list[-1].set_values(name="Tank enchantment (Mid)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Healer enchantment (Mid)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Mage enchantment (Mid)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Rogue enchantment (Mid)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Mid"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")


data_list.append(Spell())
data_list[-1].set_values(name="Tank enchantment (High)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Healer enchantment (High)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Mage enchantment (High)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Rogue enchantment (High)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("High"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")


data_list.append(Spell())
data_list[-1].set_values(name="Tank enchantment (Master)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Healer enchantment (Master)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Mage enchantment (Master)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

data_list.append(Spell())
data_list[-1].set_values(name="Rogue enchantment (Master)")
data_list[-1].set_values(category=find_cat("Enchantment"), tier=find_tier("Master"))
data_list[-1].set_values(cooldown=0, cast_time=0, max_level=10)
data_list[-1].set_values(description="""""")

for s in data_list:
	s.check()