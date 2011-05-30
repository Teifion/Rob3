import re
import database
import time
# from orders import order_utilities
from classes import order_block

from pages import common

from orders import command_o
from orders import construction_o
from orders import diplomacy_o
from orders import founding_o
from orders import relocation_o
from orders import monster_o
from orders import migration_o
from orders import military_o
from orders import operative_o
from orders import research_o
from orders import trade_o
from orders import unknown_o

from classes import res_dict

order_match_dict = {
	re.compile(r"(construction|building)"):					construction_o.Construction_block,
	re.compile(r"(diplomacy|borders)"):						diplomacy_o.Diplomacy_block,
	re.compile(r"(^research|research$)"):					research_o.Research_block,
	re.compile(r"(operatives)"):							operative_o.Operative_block,
	re.compile(r"^(trades?|city trade)$"):					trade_o.Trade_block,
	re.compile(r"^(rob command)$"):							command_o.Command_block,
	re.compile(r"(migration)"):								migration_o.Migration_block,
	re.compile(r"(coloni(s|z)ation|settlement|founding)"):	founding_o.Founding_block,
	re.compile(r"(relocation)"):							relocation_o.Relocation_block,
	re.compile(r"(monster|monsters|beasts)"):				monster_o.Monster_block,
	
	re.compile(r"(army|nav(al|y)|mobili(s|z)ation|military|recruitment)$"):	military_o.Military_block,
}

class Order_post (database.DB_connected_object):
	"""Orders post is a post containing one or more orders"""
	table_info = {
		"Name":			"orders",
		"Indexes":		{
			"turn": "turn",
			"team":	"team",
		},
		"Fields":		(
			database.Integer_field("post_id",		primary_key=True),
			database.Integer_field("turn"),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			
			database.Integer_field("topic"),
			database.Integer_field("player",		foreign_key=("players", "id")),
			
			database.Text_field("content"),
		),
	}
	
	colour_match = r'(#[a-fA-Z0-9]{1,6}|[a-zA-Z]{1,9})'
	regex_patterns = {
		"colour_match":	re.compile(colour_match),
		"size_tags":	re.compile(r'\[size=([0-9]{1,4})\](.*?)\[/size\]'),
		"boxes":		re.compile(r'\[(box|fullbox)=(%s)(,%s)?\](.*?)\[/\1]' % (colour_match, colour_match)),
		"quotes":		re.compile(r'\[quote(="([^"]*?)")?\](.*?)\[/quote\]'),
		"links":		re.compile(r'<!-- l --><a class="postlink-local" href="([^"]*)">([^<]*)</a><!-- l -->'),
		
		"order_title":	re.compile(r'^\[(o|b|u|title|h[1-5])\](.*?)\[\/(\1)\]'),
		"get_title":	re.compile(r'^\[(.*?)\]'),
	}
	
	def __init__(self, the_world, row = {}):
		self.content = ""# Force it to default to ""
		
		super(Order_post, self).__init__(row)
		
		self.blocks = []
		self.the_world = the_world
		
		self.team_ref = None
	
	
	def prep_for_split(self, content):
		"""We take in the post and create a list of blocks"""
		# Some regex patterns for later
		# colour_match		= r'(#[a-fA-Z0-9]{1,6}|[a-zA-Z]{1,9})'
		# headers_to_ignore	= r'(General orders|Specific orders|([a-zA-Z0-9\' ])*? ?Turn ?[0-9]{1,3} ?(Orders)?)'
		# 
		# # Not sure why this is in rob1
		# # $totalPost	= str_replace(':', '', $post);
		# 
		# # Remove irrelevant titles
		# content = re.sub(r'\[(o|b|title|h[1-5])\]%s\[\/(o|b|title|h[1-5])\]' % headers_to_ignore, '', content)
		
		# To save people mixing these up
		content = content.replace('[title]', '[o]')
		content = content.replace('[/title]', '[/o]')
		
		# [b][u] tags and [u][b] become just [b]
		content = content.replace('[b][u]', '[b]')
		content = content.replace('[u][b]', '[b]')
		
		content = content.replace('[/b][/u]', '[/b]')
		content = content.replace('[/u][/b]', '[/b]')
		
		# [b][o] becomes [o], yes some pepole sometimes try this
		content = content.replace('[b][o]', '[o]')
		content = content.replace('[o][b]', '[o]')
		
		content = content.replace('[/b][/u]', '[/o]')
		content = content.replace('[/u][/b]', '[/o]')
		
		# Lists are not needed
		content = content.replace('[list]', '')
		content = content.replace('[/list]', '')
		content = content.replace('[/listu]', '')
		
		content = content.replace('[*]', '')
		content = content.replace('[/*]', '')
		content = content.replace('[/m]', '')
		
		# Size tags are for losers
		# content = re.sub(r'\[size=([0-9]{1,4})\](.*?)\[/size\]', r'\2', content)
		content = self.regex_patterns['size_tags'].sub(r'\2', content)
		
		# Get rid of boxes, they don't help us work out the title
		# content = re.sub(r'\[(box|fullbox)=(%s)(,%s)?\](.*?)\[/\1]' % (colour_match, colour_match), r'\6', content)
		content = self.regex_patterns['boxes'].sub(r'\6', content)
		
		# Quotes too, they're not helpful for title calculation
		# content = re.sub(r'\[quote(="([^"]*?)")?\](.*?)\[/quote\]', r'\3', content)
		content = self.regex_patterns['quotes'].sub(r'\3', content)
		
		# Links
		# content = re.sub(r'<!-- l --><a class="postlink-local" href="([^"]*)">([^<]*)</a><!-- l -->', r'\2 (\1)', content)
		content = self.regex_patterns['links'].sub(r'\2 (\1)', content)
		
		# Remove comments too
		# content = content.replace('\n//', '//')# stops a full line comment becoming a single empty line
		# content = re.sub(r'//(.*)', '', content, re.MULTILINE)
		
		return content
	
	
	def split(self):
		the_post = self.prep_for_split(self.content)
		
		if len(the_post.split("\n")) != len(self.content.split("\n")):
			e = Exception("Error in data.order_post.Order_post.split(): len(the_post) (%s) != len(self.content) (%s)" % (len(the_post.split("\n")), len(self.content.split("\n"))))
			raise e
			
		blocks = []
		
		# Now we read through it line by line
		the_post	= the_post.split("\n")
		line_count	= len(the_post)
		
		title_type			= None
		title_name			= ''
		order_start_line	= -1
		ordrer_end_line		= -1
		title_regex			= None
		
		found_bracket = False
		
		# First we need to work out why type of titles we're using
		for l in range(line_count):
			# Human line count is l + 1
			the_line = the_post[l].strip()
			
			# Skip empty lines
			if the_line == "":
				continue
			
			if the_line[0] == "[":
				found_bracket = True
				title_type = self.regex_patterns["order_title"].search(the_line)
				
				if title_type != None:
					title_type = title_type.groups()
					title_regex = re.compile(r'^\[(%s)\](.*?)\[\/(\1)\]' % title_type[0])
					break
				
				# print(title_regex)
		
		if title_regex == None:
			if the_post == ['Orders placeholder']:
				return
			
			if 'This is the topic where you may test orders and run commands on Rob. For more information on Rob and this system, check out [url=http&#58;//woarl&#46;com/pages/rob]the Rob section on the site[/url] or chat to Teifion.' in the_post:
				return
			
			if not found_bracket:
				return
			
			print("")
			print(the_post)
			return
			raise Exception("No title regex found")
		
		for l in range(line_count):
			# Human line count is l + 1
			the_line = the_post[l].strip()
			
			# Skip empty lines
			if the_line == "":
				continue
			
			# Search for an order title here
			# title_search = self.regex_patterns["order_title"].search(the_line)
			title_search = title_regex.search(the_line)
			
			# No results found
			if title_search == None:
				continue
			
			title_type = title_search.groups()[0]
			title_name = title_search.groups()[1].strip()
			order_start_line = l
			order_end_line = 999999
			
			find = r'^\[(%s)\](.*?)\[\/(%s)\]' % (title_type, title_type)
			
			for sub_l in range(l+1, line_count):
				temp_line = the_post[sub_l].strip()
				results = re.findall(find, temp_line)
				
				if len(results) > 0:
					order_end_line = sub_l
					break
			
			# Discover the type of order we've got
			order_type = None
			for regex, class_type in order_match_dict.items():
				if order_type != None:
					continue
				
				result = regex.match(title_name.lower())
				if result != None:
					order_type = class_type
			
			# No type? Must be unknown!
			if order_type == None:
				order_type = unknown_o.Unknown_block
			
			new_block = order_type()
			new_block.the_world		= self.the_world
			new_block.team			= self.team
			new_block.title_name	= title_name
			new_block.content		= "\n".join(the_post[order_start_line+1:order_end_line])
			new_block.post			= self
			
			blocks.append(new_block)
		
		self.blocks.extend(blocks)

interactive_orders = {
	"Name":			"interactive_orders",
	"Indexes":		{
	},
	"Fields":		(
		database.Serial_field("id",			primary_key=True),
		database.Integer_field("team",		foreign_key=("teams", "id")),
		database.Integer_field("turn"),
		database.Boolean_field("handled",	default=False),

		database.Varchar_field("title",		max_length=40),
		database.Text_field("content"),
	),
}