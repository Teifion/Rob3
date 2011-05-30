from pages import common
from data_classes import spell
from queries import spell_q
import math

page_data = {
	"Title":	"Spell list",
	# "Header":	False,
	"Admin":	True,
}

def time_convert(seconds):
	# Seconds
	if seconds == 0: return "Instant"
	if seconds == 1: return "1 second"
	if seconds <= 60: return "%s seconds" % int(seconds)
	
	# Minutes
	if seconds <= 60*60:
		mins = int(math.floor(seconds/60.0))
		secs = seconds % 60
		
		# Seconds and minutes?
		if secs > 0:
			if mins == 1:
				if secs == 1:	return "1 minute and 1 second"
				else:			return "1 minute and %s seconds" % int(secs)
			else:
				return "%s minutes and %s seconds" % (int(mins), int(secs))
		else:
			if mins == 1:	return "1 minute"
			else:			return "%s minutes" % int(mins)
	
	# Hours
	if seconds <= 60*60*24:
		hours = int(math.floor(seconds/3600.0))
		
		if hours == 1:	return "1 hour"
		else:			return "%s hours" % int(hours)
	
	hours = int(math.floor(seconds/3600.0))
	if hours <= 24:
		return "%s hours" % int(hours)
	
	if hours > 24:
		extra_hours = hours % 24
		days = (hours - extra_hours)/24
	
	if extra_hours > 0:
		return "%s days and %s hours" % (int(days), int(extra_hours))
	else:
		return "%s days" % int(days)

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	spell_category = common.get_val('category', '')
	
	if spell_category != "":
		cat_id = spell.categories.index(spell_category)
		spell_selection = spell_q.get_spells_from_lore(cursor, cat_id)
	else:
		return "No handler for category '%s'" % spell_category
		# spell_selection = spell_q.spells_by_name()
	
	# spell_list = spell_q.get_spells(where="category = %d" % cat_id, orderby="tier ASC, name")
	
	output = ['<h1><a href="#top" id="top">%s magic</a></h1>' % spell_category]
	
	# Flavour/Info text
	if spell_category == "Light":
		output.append("""
		""")
	
	elif spell_category == "Dark":
		output.append("""Dark magic is by no means "bad" or "evil", it is magic focused on avoiding direct conflict with an opponent and often works in a sublte manner.
		""")
	
	elif spell_category == "Destruction":
		output.append("""
		""")
	
	elif spell_category == "Abjuration":
		output.append("""
		""")
	
	elif spell_category == "Daemonic":
		output.append("""
		High and master tier mages are assumed to have twice the control over a mid tier daemon than a mid tier mage. Tier of mage has no effect on the possession type daemons.
		<br /><br />
		
		Daemonic progression makes a daemon more powerful but at the cost of magic, using magic reduces their Strength and Agility. The amount reduced is equal to the chance to miscast, a 50% chance to miscast halves their strength and agility. Each stage of the progression increases the cap by 20% (ascension is stage 3 and thus the cap is 60%, you can't lose more than 60% of your strength and agility when ascended). Daemons below the cap suffer no ill effects from miscasting a low or mid tier spell and reduced effects from miscasting high and master tier spells.
		""")
	
	elif spell_category == "Necromancy":
		output.append("""
		""")
	
	elif spell_category == "Animation":
		output.append("""
		Animation is an exclusive lore, you cannot practice animation while you practice any other lore.
		<br /><br />

		Any animation has two parts; the physical object and the spells. The object is controlled and moved by the spells and as a result becomes animated. Below is a simple tutorial on how to create an automated catapult.
		<br /><br />
		
		<div class="listblock" style="background-color: #FEF; border-color: #A0A;">
			The physical object is a standard catapult, it's expected to have the 4 wheels for movement on it's base and fires using a large spoon that impacts against a wooden cross-beam to release a projectile. The one alteration is that the axel connected to the spoon shall be connected via a chain to a set of 6 other rotating beams allowing them to drive the firing of the device.
			<br /><br />
			
			<strong>Movement</strong><br />
			Each of the 4 wheels shall have a rotary motor connected to a gearing system for moving heavy loads.
			<br /><br />

			<strong>Firing mechanism</strong><br />
			Each of the six additional rotating beams will have a rotary motor connected to a catalyst allowing for a sudden burst of speed and thus driving of the mechanism.
			<br /><br />
			
			<strong>Cognition</strong><br />
			The device shall have a Basic cognition placed within it. The first command is "fire":
			<ul>
				<li>All 6 firing beams will activate and spin at maximum speed so as to rotate the spoon from horizontal to vertical</li>
				<li>As soon as power is exhausted from the beam motors they will cease, gravity will pull the spoon back down and it can be manually loaded</li>
			</ul>
			
			The second command is "move", to use it a direction of forwards or backwards must be given:
			<ul>
				<li>The wheel motors activate and rotate in a direction that moves the catapult in the direction specified.</li>
				<li>Upon exhaustion the motors will rest until at full power and resume, this continues until the move command is cancelled.</li>
			</ul>
		</div>
		<br />
		
		This is just a simple example missing out many of the things possible to do with animation.
		<br /><br />
		
		<h3><a href="#all" id="all">Notes on all spells</a></h3>
		All animate spells have no range, they requrie the animator to be touching the object when casting though after this the animation can move as far as wanted from any of it's animators. Note that controlling an animation requires a form of cognition or mental link each of which have their own limitations described as part of the spell.
		<br /><br />
		
		Animations take 30 minutes to cast and take 2 hours to become active subsequent to casting, multiple animations can be cast upon a single object at once. An animation will expire only when the animator casts a new spell, dies or if the link is severed. The link is magical in nature and follows the (hidden) rules for magical links.
		<br /><br />

		Multiple motors can be attatched to a single joint and can work in parallel to give more power or in sequence to give a longer duration.""")
	
	elif spell_category == "Sourcery":
		output.append("""
		
		""")
	
	output.append("<br />")
	
	last_tier = -1
	
	for spell_id, the_spell in spell_selection.items():
		
		# Check for tier change
		if last_tier != the_spell.tier:
			output.append('<br /><h4><a href="#%(tier)s" id="%(tier)s">%(tier)s tier spells</a></h4>' % {
				"tier":	spell.tiers[the_spell.tier]})
			
			last_tier = the_spell.tier
		
		# Spell output
		output.append("""<strong><a href="#%(name)s" class="clear_link" id="%(name)s">%(name)s</a></strong>
		<span style="font-size: 0.9em;">
			&nbsp;&nbsp;&nbsp;Cooldown: %(cooldown)s
			&nbsp;&nbsp;&nbsp;Cast time: %(cast_time)s
		</span>
		<br />
		%(description)s
		<br /><br />""" % {
			"name":			the_spell.name,
			"description":	the_spell.description.replace("\n", "<br />"),
			"cooldown":		time_convert(the_spell.cooldown),
			"cast_time":	time_convert(the_spell.cast_time),
		})
	
	return "".join(output)

