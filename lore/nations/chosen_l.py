data = {
	"cat":	"nations",
	"page":	"chosen",
}

blocks = [
	{
		"id":		"overview",
		"title":	"",
		"text":		"""
		Each nation has within it tens or hundreds of thousands of civilians and soldiers. It also has a leader, this leader is you. Your character is a Chosen One, a supernaturally powerful being. If there is more than one player on a team then they each have a Chosen One. A Chosen One is still the same race as the rest of their nation, they are simply far stronger, faster and smarter.
		<br /><br />

		<div class="advanced">
			When a Chosen One moves team they do not take with them knowledge from the other team. This means that if you move from one team to another you cannot use information gleaned while on that other team. Note that the is In Character information, you are more than welcome to put to use the skills and talents for orders that you learnt on another team into action.
		</div>

		<?php
			echo addHeading('Faster, stronger and tougher');
		?>
		<img src="../../images/nations/might.png" alt="" width="134" height="180" style="float: right;"/>
		Chosen are physically superior to the rest of their race. Chosen are four times as strong, twice as tough and able to run and fight for four times the length of time any of their race can.
		<br /><br />

		Chosen improve over time, the more the chosen achieves the more that they improve. The improvements are measured in levels; to move up a level the Chosen must kill another Chosen. They can either do this with their weapon, with a spell or with an army. However, a Chosen will can only go up one level from a given kill, repeatedly killing the same enemy over and over again will net them no extra reward in levels. These levels are covered in the <a href="feats.php">Chosen One feats</a> page.
		<br /><br />

		<?php echo addHeading('Death'); ?>
		At some point, your Chosen will die. The good news is that this is (probably) not permanent. Firstly there is the <a href="../magic/creation.php#resurrection">resurrection</a> spell. Secondly, all Chosen will be resurrected automatically as part of who and what they are. This takes exactly 12 months from the moment of death plus one more month for each level that the Chosen has. A level 12 Chosen takes 2 years to resurrect.
		<br /><br />

		<div class="advanced">
			Imprisoning a Chosen to prevent resurrection will not work, they will find a way to kill themselves and thus be brought back to life. I'm aware this seems to be quite limiting but it was agreed upon by a lot of people to be a good rule as it ruined a large amount of the game for those captured like that.
		</div>
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