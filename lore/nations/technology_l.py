data = {
	"cat":	"nations",
	"page":	"technology",
}

blocks = [
	{
		"id":		"overview",
		"title":	"",
		"text":		"""
		<img src="../../images/nations/technology.png" width="110" height="111" style="float: right;"/>
		To research technology you must have a university, each university creates research points which last for that turn and that turn only. The points are recreated each turn so you must use them or lose them. Initially you must spend some materials to fund this research and so each technology has a cost in both materials and university power.
		<br /><br />

		If you do not have enough points to research a technology in one turn then it is left partially completed, you will <strong>not</strong> have to pay the material cost again next turn. Most technologies have multiple levels of power and you can research it several times.
		<br /><br />

		<div class="advanced">
			The system is designed so that each level of a technology will require you to pay more than the last and thus giving your a worse cost/benefit ratio.
		</div>

		<?php
			echo addHeading('What are the technologies?');
		?>
		The technologies are listed below along with their effect and costs. The cost equations use L to represent the level that you are researching. To save you needing to do this yourself you can enter the level into the textbox and it will tell you how much it will cost to move from the level below to the level that you enter. Technologies without an L in the equation are a super-tech and cannot be taken past level 1.
		<br /><br />

		<table border="0" cellspacing="0" cellpadding="5">
			<tr class="row2">
				<th>Technology</th>
				<th>Materials cost</th>
				<th>Research cost</th>
				<th>Bonus</th>
				<th>Level</th>
				<th>Cost</th>
			</tr>

		<?php

		print `curl -d mode=tech_display -d ajax=True http://localhost/rob3/web.py`;

		?>

		</table>
		<br />

		If you are mid-way through researching a tech and want to research a different one, your progress on the old one will be kept and you can come back to it later.
		<br /><br />

		<?php echo addSubHeading('Gunpowder'); ?>
		Gunpowder has up to 3 levels available to it. After the first level you can create Arquebus, with a second level you can create primitive rockets and with a third level you can create muskets.
		<br /><br />

		<?php
			echo addHeading('Trading');
		?>
		One of the most useful things about allies is that they very often have different techs to yourself. If they have a higher level of a tech than you then they can give you up to one level at a time towards it until you reach the same level as them. Each team may give two techs/spells away each turn, "supertechs" may not be traded.
		<br /><br />

		<?php echo addHeading('Nomads'); ?>
		Nomads are unable to construct universities and thus cannot research mundane technologies. Nomadic cities also have no way to use the technologies even if they were traded to them. A partially nomadic nation can however partially use make use of some of the technologies in their non-nomadic cities.
		"""
	},

	{
		"level":	"secret",
		"text":		"Secret info"
	},
	{
		"id":		"gm_notes",
		"level":	"gm",
		"text":		"GM info"
	}
]