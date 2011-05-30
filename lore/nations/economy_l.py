data = {
	"cat":	"nations",
	"page":	"economy",
}

blocks = [
	{
		"id":		"overview",
		"title":	"",
		"text":		"""
		<?php
			echo addHeading('Resources');
		?>
		World of Arl has two main resources: food and matearials. Food cannot be stored for long and any you had at the end of one turn does not carry over to the next. Materials on the other hand can be stored up. There are in addition three other elements called Supplies, they are Wood, Stone and Iron but we'll come on to them later.
		<br /><br />

		<?php
			echo addSubHeading('Cities');
		?>
		Each city on the landmass produces a certain amount of food, a certain amount of materials and can have access to one of the three supplies. For those that are like me and can't remember how to read a grid reference, X is a-cross and the alphabet goes vw<strong>XY</strong>z. So X is across and goes before Y.
		<br /><br />

		<div class="advanced">
			Cities are shown on the map by a square with the team colours and the team icon. The larger the square the larger the city. If you move your mouse over a city icon then a box will pop up showing information about the city.
			<br /><br />

			Clicking a part of the <a href="../../map">map</a> will give you the coordinates of the location that you clicked on.
		</div>

		<?php
			echo addHeading('Food');
		?>
		Food is used to feed your people, you can't have too much food but if you have lots of it then your people will be happier and your troops have more morale. Not enough food and they can riot, defect and starve to death. Being short of even a little food will lower your rate of population growth.
		<br /><br />

		Most cities produce more food than they need which is important for feeding the military. Bigger cities do not always produce enough food for themselves so it can be important to have some smaller cities to supply the bigger ones. Food can be transported so if you do not have enough food, it is possible to buy, steal or beg food from another country.
		<br /><br />

		<div class="advanced">
			Food is automatically shared between your cities so any cities that don't have enough will use the surplus from those that do.
			<br /><br />

			The first 50,000 people in a city will produce 150% of the food they need. The next 5,000 people in the city will produce a little less and the next 5,000 less still. Any people after 100,000 will not produce food. This means that the most efficient way to produce food is with smaller cities but that you can also have larger ones.
		</div>

		The amount of food produced by a city can be increase with the <a href="evoList.php#affinityfortheland">affinity for land</a> evolution or with the <a href="technology.php#farming">farming tech</a>
		<br /><br />

		<?php
			echo addHeading('Materials and Growth');
		?>
		Each city also produces materials, but the more materials it produces the slower it grows. Small (15,000) cities will grow by a larger percentage while a larger (50,000) city will produce more materials but grow more slowly or even shrink if it is too large.
		<br /><br />

		<div class="advanced">
			Materials produced are equal to sqrt(size * size * 4.5) - 25. It probably looks confusing, all you need to worry about is that bigger cities produce more materials.
			<br /><br />

			Population grows at a percentage rate of 8 - ((Size - 20) * 0.2)
		</div>

		<?php
			echo addHeading('Supplies');
		?>
		<div style="float: right; text-align: center;">
			<img src="../../images/nations/supplies.png" width="45" height="42" />
			<br /><br /><br />
			<img src="../../images/nations/terrain.png" width="61" height="58" />
		</div>
		Aside from food and materials, you also have supplies. With a supply you either have it or you do not; you never have a limited amount of it nor a surplus of it. Supplies make it cheaper and easier to do things, without iron your metal weapons and armour are more expensive. Without wood your ships take longer to build and without stone you both cannot build walls and your normal buildings take longer to build.
		<br /><br />

		Supplies are thus useful things to have. Supplies are map specific, stone comes from mountains, iron from hills and wood from forests. But not all mountainous cities provide stone, not all hilly cities iron and not all forests wood. Supplies are marked on the map by a round orb, red for iron, grey for stone and green for wood.
		<br /><br />

		<div class="advanced">
			Supplies can be transported over water and land, if you have one city on an iron supply then your nation counts as having iron. If that city is cut off from the rest then you will not benefit from it's supply. Cities can be cut off by enemy forces so it's important to ensure that you can defend your cities.
			<br /><br />

			The second set of icons on the right are terrain types. The trapezoid is a giant hill, the octagon fertile land and the C shape a natural harbour. Giant hills are easy to defend, fertile land produces twice the food and natural harbours are easier to defend against sea invasion.
		</div>

		<?php
			echo addHeading('Economic warfare');
		?>
		As everything you do costs a certain amount of materials, if you can deprive an enemy of their materials then they will be unable to buy as much as normal. However, materials are not normally left lying around and is thus not very easy to steal. Much easier is to prevent them from getting the supplies that they require.
		<br /><br />

		Assume if you will that "Ranil" control an iron mine and are happy to trade with "Amarr". Amarr don't have any supplies of iron for themselves and thus rely on Ranil to supply them with iron. If you wanted to strike at Amarr, stopping the supply trains from Ranil to Amarr will remove Amarr's supply of Iron and they will be forced to pay through the nose for Iron weapons.
		<br /><br />

		<div class="advanced">
			If a team runs low on materials by enough or for long enough then their people's morale will drop and it's far easier to invade (less militia) and to perform sedition.
		</div>

		<?php
			echo addHeading('Being a supplier');
		?>
		Supplies can be shared with anybody that has a connection to your supply location, be it over land, sea or a combination of the two. If you have a supply then you can share it with as many nations as you like, remember that supplies are either a have or a have not, you do not have a limit on them. By the same logic however, having 4 supplies of wood gives no advantage over having just 1.
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