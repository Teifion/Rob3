# TODO format page
data = {
	"cat":	"general",
	"page":	"orders",
}

blocks = [
	{
		"id":		"overview",
		"title":	"Orders",
		"text":		"""Orders are what you tell your nation to do. You can order the founding of new cities, the construction of great walls, the conscription of a new army and the designing of a giant metal spider with death rays. An order is simply an instruction, more complicated orders need also to have instructions on how to achieve them but we'll come to that later.
		<br /><br />"""
	},
	{
		"id":		"how",
		"title":	"How to write orders",
		"text":		"""
		There are two types of orders, normal orders and international orders. The normal orders deal with the running of the nation while the international orders deal with other nations. There is however an exception to this rule, trading must be placed in normal orders unless it's a special trade.
		<br /><br />
		
		<div class="advanced">
			Trades are placed in normal orders because normal orders are always worked out before international orders. This means that to benefit from resources or research sent by another nation you must receive it first thing, thus it must go in normal orders.
		</div>
		
		All orders should be as factual as possible, it can be fun to tell a story of your nation and what it does but orders are instructions. These instructions are carried out by me and my getting confused translates directly into your people getting confused. Assuming that your order was clear and a mistake is still made, contact me before the next turn and I'll clear it up, I'm human and make mistakes like everybody else.
		"""
	},
	{
		"id":		"normal",
		"title":	"Normal orders",
		"text":		"""
		Most normal orders are not performed by me, they're performed by a computer program called Rob. These orders need to follow a simple template and covered fully in the <a href="../rob">Rob the Database</a> section. The orders are quite readable and if you didn't know that they had to follow a template you may never notice it was there.
		<br /><br />
		
		Some orders however are simply not part of the normal day-to-day operation of a nation. These are the creative orders, the orders such as the construction of a giant metal spider with death rays. These orders are not handled by a computer program, they are handled by myself and covered in more detail in the <a href="crazy.php">crazy projects</a> section."""
	},
	{
		"id":		"intenationl",
		"title":	"International orders",
		"text":		"""
		These are the orders that bring down nations, the orders that you use to defend your nation from invasion or to come to the aid of an ally. A large part of the fun of the game is that you have a lot of freedom with these orders, you don't need to invade in a specific way, it's up to you to decide how you do things.
		<br /><br />
		
		Owing to the openness of the game there's no specific list of categories for international orders. As there is no list I have simply listed the most common types here."""
	},
	{
		"id":		"invasion",
		"title":	"Invasion",
		"text":		"""
		An invasion requires a target, a list of what you will invade with (give army names, not specific troop types) and how you will do it. Optionally you can include more specific things such as what time of the year your forces will depart and what route they will take. When your forces arrive at their location the orders should explain how they will attack, you don't need to go into minute detail but neither should you leave it at "take their city".
		"""
	},
	{
		"id":		"assassination",
		"title":	"Assassination",
		"text":		"""
		The age old tactic of killing the leader of the opposition. Your orders should detail how you will find your target (some are easier to find than others) and if needed, how you will kill them. Sometimes it's acceptable to write "stab them" but sometimes you're unable to make it that simple, it all depends on the target. Optionally you can include escape orders too."""
	},
	{
		"id":		"defence",
		"title":	"Defence",
		"text":		"""
		If you know someone is attacking you then you can counter this. You can leave specific or general orders for dealing with attacks in a specific way. If you know your opponent will use catapults to knock down your walls then you can leave orders to keep light cavalry outside of the city and to harass their siege engines once the siege begins."""
	},
	# {
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