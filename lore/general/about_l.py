# TODO Format page
data = {
	"cat":	"general",
	"page":	"about",
}

blocks = [
	{
		"id":		"overview",
		"title":	"The 3 step guide to playing",
		"text":		"""
		World of Arl is a turn based strategy game. Each player either has their own nation or is a secondary leader of another nation. Each game turn lasts a year of game time, during the turn your nation performs actions. Some of the actions are automatic such as production of materials and food, some are not. These non-automatic actions are what you are there for, you must order your nation as you see fit.
		<br /><br />

		<?php
			echo addSubHeading('What sort of actions?');
		?>
		There are two types, normal and international. Normal orders take care of the internal development of your nation with construction, research and recruitment to name the three most common. It is however the international that makes the game so much fun. While there are only so many types of building that you can build, there is nearly no limit on how many different ways you can attack someone. There are options besides attacking people and they are up to you to decide upon.
		<br /><br />

		<?php
			echo addSubHeading('How does it work?');
		?>
		The game is run by a single person (me, Teifion) with the assistance of a computer program called Rob the Database. Each turn I run through all the orders written and play them out. The results of your orders are posted to your private team forum and also to a public report.
		<br /><br />

		<?php
			echo addHeading('I want to start playing');
		?>
		Brilliant! I would head over to the "<a href="starting.php">how to start playing</a>" page which has an itemised list of what you need to and can do to start playing the game as soon as possible.
		<br /><br />
		"""
	},	# {
	# 	"level":	"secret",
	# 	"id":		"",
	# 	"text":		""
	# },
	# {
	# 	"id":		"gm_notes",
	# 	"level":	"gm",
	# 	"text":		"GM info"
	# }
]