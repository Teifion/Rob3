data = {
	"cat":	"nations",
	"page":	"evolution",
}

blocks = [
	{
		"id":		"overview",
		"title":	"",
		"text":		"""
		Your nation begin as humans but over the course of playing, change into something else. This is done through the earning of evolution points. Points are earned through action and achievement, you do not have to win to evolve but it does help.
		<br /><br />

		<?php
			echo addSubHeading('What can be done');
		?>
		There is a massive range of what can be done to your race, you can make it breathe underwater, you can give them wings, you can change the length of their arms and legs and you can make them smarter or stupider. It's an incomplete list but hopefully gives you some idea of the things you can do. For things we've not already thought of there is also the ability to add your own evolution idea.
		<br /><br />

		<?php
			echo addHeading('How does it work?');
		?>
		As you play, you will receive evolution points for achievements. The points can be spent at any time (contact a GM to get it done) and can also be saved up for the bigger and more expensive evolutions. Once you get your points you simply need to pick the evolution you want from the <a href="evoList.php">list of evolutions</a>, if you don't find one you want then contact me and we'll work one out.
		<br /><br />

		<?php
			echo addSubHeading('Getting points');
		?>
		Every 5th turn points are distributed to nations that achieve objectives, you cannot get more points for non-war things than for wars. This means that if you participate in no wars you get no evolution points. The objectives are listed below, if you can think of additional ones to add then please don't hesitate to suggest any.
		<br /><br />

		<div style="float: right; width: 200px;">
			<ul>
				<li>Largest army</li>
				<li>Largest navy</li>
				<li>Most mages</li>
				<li>Most operatives</li>
			</ul>
		</div>

		<ul>
			<li>1 Point for each war (max 5, 1 per turn)</li>
			<li>Control one of each supply (2 points)</li>
			<li>Most slaves</li>
			<li>Most civilians</li>
			<li>Good team role playing</li>
		</ul>
		<br />

		<?php echo addHeading('Spending'); ?>
		After you get the points you may spend them at any time. Simply inform me of what you wish to purchase and everything will be sorted out. For a list of evolutions, look <a href="evoList.php">here</a>.
		<br /><br />

		<?php echo addSubHeading('Respending'); ?>
		So, what happens when you decide that the 10 levels of strength are nice, but could be better spent? You can sell off what you bought but only at half the price of what you paid for them.
		<br /><br />

		<?php echo addSubHeading('Materials'); ?>
		It is possible that you do not wish to spend or horde your evolution points and instead wish to remain as you are. You can exchange 1 evo point for a 20% boost to your materials generation for that turn, 5 evo points will double your material production. As evolutions are done after orders, you will know exactly how much you will get and how useful it will be.
		<br /><br />

		<?php echo addHeading('Negative evolutions'); ?>
		It's quite plausible that you might want to make your race disadvantaged in a certain area. This is called negative evolution. Whenever you spend a point of evolution, you may spend a negative evolution point and take a negative point in another evolution. This will give you a free extra point to spend (though you can't get another negative point from this one). If you later change your mind on a negative evolution, you must "buy it out" with evolution points at full price.
		<br /><br />

		<div class="advanced">
			If you have 10 points to spend you cannot take it further than 20 positives and 10 negatives, you cannot end up with more than twice as many positives as you have to start with.
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