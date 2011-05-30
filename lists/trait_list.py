import database
from data_classes import trait

cat_lookup = trait.categories.index

class Trait (database.DB_list_row):
	defaults = {
		"show":		True,
	}
	
	# def __init__(self, **kwargs):
	# 	super(Trait, self).__init__(**kwargs)
	# 
	# def check(self):
	# 	pass

data_list = []

#	Government
#------------------------
data_list.append(Trait(
	name		= "Dictatorship",
	category	= cat_lookup("Government"),
	description	= """The government is ruled by one man and one man only. It has no in-game advantages or disadvantages.""",
))

data_list.append(Trait(
	name		= "Monarchy",
	category	= cat_lookup("Government"),
	description	= """The government is ruled by a family who inherit power from their parents. The upshot is that people believe that their rulers have a right to power yet such a right can quickly fall away if assassinated and riots much more likely to start.""",
))

data_list.append(Trait(
	name		= "Democracy",
	category	= cat_lookup("Government"),
	description	= """Leaders are elected by the people and as a result gives a boost to happines to all cities large enough to have a representative. The smaller cities however find themselves ignored in lawmaking and will feel unhappy as a result.""",
))

data_list.append(Trait(
	name		= "Rule of might",
	category	= cat_lookup("Government"),
	description	= """The chieftain is the strongest member of the race. He or She leads by example in all things, but primarily in defending the nation from threats. When going into battle the nation is inspired by the Chieftain if he leads them into battle, however if he does not, then the troops are more liable to run, additonally their death will cause a larger morale drop. This has no effect on city happiness.""",
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Government"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Government"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Government"),
	description	= """ """,
	show		= False,
))

#	Religion
#------------------------
data_list.append(Trait(
	name		= "Free religion",
	category	= cat_lookup("Religion"),
	description	= """Anything and everything is an idol of worship. Temples are irrelevant and no formal worship system is organised. Religiously provoked riots are nearly impossible to create but no deity will accept followers who see them on a par with a powerless spirit.""",
))

data_list.append(Trait(
	name		= "National religion",
	category	= cat_lookup("Religion"),
	description	= """The nation as a whole follows one or more deities and in return can earn their favour and reward. While the deity is happy the people are happy and when the deity is unhappy, so are the people. In the case of multiple deities the most displeased deity will have the greatest effect on the people.""",
))

data_list.append(Trait(
	name		= "Atheism",
	category	= cat_lookup("Religion"),
	description	= """The nation refuses to acknowledge the divinity of any of the so called "deities" and instead worships nobody. With no deity to please the nation can focus on other things yet does not benefit or disadvantage from the lack of a patron. The downside is that some deities will view atheism as a favourable target for their own followers.""",
))

data_list.append(Trait(
	name		= "Chosen deity",
	category	= cat_lookup("Religion"),
	description	= """The nation sees it's leader as a deity and worship them. Any action led by such a figure has a much higher morale boost but at the same time a much higher morale hit if the leader is slain. Additionally some deites may consider an individual such as this to be a threat.""",
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Religion"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Religion"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Religion"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Religion"),
	description	= """ """,
	show		= False,
))

#	Society
#------------------------
data_list.append(Trait(
	name		= "Slavery",
	category	= cat_lookup("Society"),
	description	= """Lower classes have no rights and all labour is either very cheap or even free. Cities produce an extra 20% materials but riots are 100% more likely to start if there is no slave prison in the city.""",
))

data_list.append(Trait(
	name		= "Serfdom",
	category	= cat_lookup("Society"),
	description	= """Workers have some rights but the rich typically remain rich and the poor poor. As long as the workers remain happy enough to work there are no riots.""",
))

data_list.append(Trait(
	name		= "Caste system",
	category	= cat_lookup("Society"),
	description	= """People are born into their role and there is little to no chance of them moving to a higher social status. The people are half as likely to riot but it is an inefficient way to do things and all cities produce 20% fewer materials.""",
))

data_list.append(Trait(
	name		= "Emancipation",
	category	= cat_lookup("Society"),
	description	= """People are free to decide their own path and job in life. As a result everybody is naturally happier as they feel in control, however when the public become unhappy they are far more likely to riot as they choose for themselves.""",
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Society"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Society"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Society"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Society"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Society"),
	description	= """ """,
	show		= False,
))

#	Natural focus
#------------------------
data_list.append(Trait(
	name		= "Warlike",
	category	= cat_lookup("Inclination"),
	description	= """A warlike nation enjoys and thrives on wars and conflict, wars will not have the negative effect as normal though an extented period of peace can bring about it's own unhappiness.""",
))

data_list.append(Trait(
	name		= "Mercantile",
	category	= cat_lookup("Inclination"),
	description	= """Money and wealth are sought after things and wealthy cities will feel happier as a result, those that are not wealthy will by contrast be unhappy.""",
))

data_list.append(Trait(
	name		= "Sailors",
	category	= cat_lookup("Inclination"),
	description	= """The nation is at home on the waves of the oceans and ports bring happiness to the people, inland cities however will bring about unhappiness.""",
))

# data_list.append(Trait(
# 	name		= "Magicians",
# 	category	= cat_lookup("Inclination"),
# 	description	= """ """,
# ))

data_list.append(Trait(
	name		= "Educated",
	category	= cat_lookup("Inclination"),
	description	= """The people consider themselves well educated and informed about life, universities and academies of magic confer a happiness bonus while a lack of them will displease a people.""",
))

data_list.append(Trait(
	name		= "Peaceful",
	category	= cat_lookup("Inclination"),
	description	= """Wars are a waste of valuble lives and materials, avoiding them makes the people happy while going to war is a saddening event.""",
))

data_list.append(Trait(
	name		= "Expansionist",
	category	= cat_lookup("Inclination"),
	description	= """The people will not remain content to occupy only a small slip of land, any city over a certain size will desire to expand it's borders and found new cities. Smaller cities feel happy with their progress and are thus happier. Additionally cities younger than 5 years old will be happier.""",
))

data_list.append(Trait(
	name		= "Paranoid",
	category	= cat_lookup("Inclination"),
	description	= """The people need to be reassured of their saftey, they take far more comfort in a military guard being present but become far more worried without one. A reasonable size of garrison is 10% of the size of the city.""",
))

data_list.append(Trait(
	name		= "Pious",
	category	= cat_lookup("Inclination"),
	description	= """Religion plays a large part in the lives of the people. While shrines and small places of worship are not hard to come by for anyone, the people grow happier when there is a centralized place for worship. The presence of Temples and Expanded Temples increases the happiness of the people in that city, while their absence decreases happiness.""",
))

data_list.append(Trait(
	name		= "Hygienic",
	category	= cat_lookup("Inclination"),
	description	= """The people care more about hygiene than other people. They will be more happy in a city with hospitals and sewer systems than in one without them.""",
))

data_list.append(Trait(
	name		= "Well fed",
	category	= cat_lookup("Inclination"),
	description	= """The people are used to an abundance of food. As a result they are more happy and carefree normally, but grow unhappy faster when food supplies are low (eg might require at least 10% surplus of food).""",
))

data_list.append(Trait(
	name		= "Zealous",
	category	= cat_lookup("Inclination"),
	description	= """Most people follow their deity or detiies with fervent passion; to them their deity is more than 'just' a patron - and they expect the same of their leaders. If the Chosen abide to the deity's wishes and further the divine one's goals, then the people too will be happy. However, if the Chosen Ones fail to the deity's wishes or, Arl forbid, even go against the deity's wishes, then trouble will brew.
	The effects of this trait stack with that of national religion.""",
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))

data_list.append(Trait(
	name		= "VOID",
	category	= cat_lookup("Inclination"),
	description	= """ """,
	show		= False,
))