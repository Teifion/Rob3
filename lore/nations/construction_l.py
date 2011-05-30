data = {
	"cat":	"nations",
	"page":	"construction",
}

blocks = [
	{
		"id":		"overview",
		"title":	"",
		"text":		"""
		Your cities will automatically expand to accommodate extra people. Cities are however not very easy to defend, they don't have the nice walls that castles do and as such it's a good idea to build walls. Walls make a city far easier to defend. The larger the walls the more people that can fit inside them. Walls are called by their size, "50k Walls" means walls able to hold 50,000 people or 100,000 for a shorter space of time.
		<br /><br />

		<div class="advanced">
			City fighting is nasty and generally both slow and costly for both sides involved. Putting walls on your cities will allow the militia to be able to help far more as well as allowing a garrison to hold out against a far larger army.
		</div>

		<?php echo addSubHeading('Fortifications'); ?>
		Walls alone are pretty good. Better still is the adding of fortifications to them. A fortified city is very easy to hold and anybody attacking it can expect high casualties. Fortifications are named in the same way as walls but are an upgrade from walls, you must build walls before fortifications.
		<br /><br />

		<div class="advanced">
			Fortifications massively improve the defensive power of a wall. The defending force can hold out against a very much superior attacking force.
		</div>

		<?php echo addHeading('Founding'); ?>
		<img src="../../images/nations/expansion.png" alt="" width="188" height="129" style="float: right;"/>
		Founding new cities is not without a cost. Those founding a new city or moving from one city to another will not produce materials that turn. This goes down as a cost but only so that it's easier to track, no harm will come from going over-budget by that amount.
		<br /><br />

		<div class="advanced">
			Cities cannot build on the turn that they are founded.
		</div>

		<?php echo addSubHeading('Terrain features'); ?>
		<img src="../../images/nations/terrain.png" width="61" height="58" style="float: right;"/>
		Some parts of the map have special features that give them some kind of a bonus. These take the form of a flat topped pyramid for a giant hill, a very dark green octagon for fertile land and a lime C for natural harbours.
		<br /><br />
		<ul>
			<li>Giant hills are much easier to defend owing to the height advantage enjoyed by your city</li>
			<li>Cities built on fertile plains produce twice as much food as normal</li>
			<li>Cities built on a natural harbour have a much better protected port area</li>
		</ul>
		<br />

		<?php echo addHeading('Normal buildings'); ?>
		To build ships you need a shipyard, to research magic you need an academy and so on. Buildings are built over a period of turns and cost 5 materials each turn building work takes place on them. Only one of each building can be constructed at each city though some buildings can be expanded. Each city may only build one building per turn and only one wall per turn.
		<br /><br />

		Below are the most common buildings, for a full list I suggest you look at the <a href="constructionFull.php">full building list</a>.
		<br /><br />

		<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
			<tr class="row2">
				<th class="empty">Building</th>
				<th class="empty">Purpose</th>
			</tr>
			<tr class="row0">
				<td>Shipyard</td>
				<td>Produces 100 shipbuilding points</td>
			</tr>
			<tr class="row1">
				<td>University</td>
				<td>Produces 50 research points</td>
			</tr>
			<tr class="row0">
				<td>Magical academy</td>
				<td>Produces 50 spell points</td>
			</tr>
			<tr class="row1">
				<td>Temple</td>
				<td>Produces 1 favour point</td>
			</tr>
			<tr class="row0">
				<td>Castle</td>
				<td>Holds 5,000 people (very hard to breach)</td>
			</tr>
		</table>
		<br />

		If you do not have a supply of stone to the city then buildings take twice as long to build and walls cannot be built at all.
		<br /><br />

		<?php echo addHeading('Nomads'); ?>
		Nomadic "cities" cannot construct buildings but are able to migrate each turn. Nomadic cities may migrate as fast as heavy infantry can march, nomadic cities produce half the resources of normal and fewer the further they migrate each year. In addition a Nomadic city cannot grow larger than 30,000 people.
		<br /><br />

		<div class="advanced">
			Nomads are harder to play than a normal nation, they cannot build walls and thus their defense is to run away from their opponents.
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