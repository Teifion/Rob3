import re
import database
import time
# from orders import order_utilities

from pages import common

# from orders import chosen_orders
# from orders import command_orders
# from orders import construction_orders
# from orders import diplomacy_orders
# from orders import disbanding_orders
# from orders import enchantment_orders
# from orders import founding_orders
# from orders import intelligence_orders
# from orders import relocation_orders
# from orders import mage_orders
# from orders import migration_orders
# from orders import military_orders
# from orders import operative_orders
# from orders import research_orders
# from orders import trade_orders
# from orders import unknown_orders
# 
# from orders import military_orders_new as military_orders

from classes import res_dict

order_match_dict = {
	"construction":	r"(construction|building)",
	"disband":		r"(disband)",
	"diplomacy":	r"(diplomacy)",
	"research":		r"(spell|magic|mundane|tech|research)",
	"operatives":	r"(spies|operatives|covert|agents|subterfuge|mission)",
	# "mages":		r"(train )?(magi|mage|wizards)",
	"trades":		r"(trade|trading|resources)",
	"enchantment":	r"(enchantment)",
	"chosen":		r"(chosen|personal|level advancement)",
	"command":		r"(rob command)",
	"migration":	r"(migration)",
	"founding":		r"(coloni(s|z)ation|settlement|founding)",
	"intelligence":	r"___XYZ___",# Spy stuff
	"relocation":	r"(relocation)",
	
	"military":		r"(beasts|army|nav(al|y)|mobili(s|z)ation|military|recruitment|training|troops|ships|airship|warriors|mage|magi|armies)",
}

class Order_block (object):
	"""docstring for Order"""
	def __init__(self, team=-1, title_name="", content=""):
		super(Order_block, self).__init__()
		self.content	= content
		self.title_name	= title_name
		self.order_type = ""
		
		self.team		= team
		self.team_ref	= None
		self.cost		= res_dict.Res_dict()
		
		self.results			= ""
		self.queries			= []
		self.input_response		= []# errors and such found on lines
		self.formatted_content	= ""# content with formatting from the order reader
		
		# Only applies to trades
		self.results_for_others = {}
		self.queries_for_others = {}
	
	def get_type(self):
		if self.order_type != "": return self.order_type
		
		# Match it from the start of the string
		for k, v in order_match_dict.items():
			result = re.search("^%s" % v, self.title_name, re.IGNORECASE)
			if result != None:
				self.order_type = k
				return self.order_type
		
		# Match it from anywhere in the string
		for k, v in order_match_dict.items():
			result = re.search(v, self.title_name, re.IGNORECASE)
			if result != None:
				self.order_type = k
				return self.order_type
		
		# We have an issue, must be unknown
		self.order_type = "unknown"
		return "unknown"
	
	def find_match_in_string(self, needles_ids, needles_names, haystack, strictness=1, loop_all=False):
		"""Finds one of the dict"""
		if loop_all:
			strict_min = 1
		else:
			strict_min = strictness
		
		# Strictest search, needs to find something identical
		if strict_min <= 1 and strictness >= 1:
			grep_pattern = r"\b(%s)\b" % "|".join(needles_names)
			
			result = re.search(grep_pattern, haystack, re.IGNORECASE)
			if result != None:
				found_name = result.groups()[0]
				if found_name in needles_names:
					return needles_ids[needles_names.index(found_name)]
				else:
					# It's of a different case, need to do this the long way
					lower_key = found_name.lower()
					for k in needles_names:
						if lower_key == k.lower():
							return needles_ids[needles_names.index(k)]
		
		# Take out some characters, it might be something odd like that
		if strict_min <= 2 and strictness >= 2:
			return -1
		
		if strict_min <= 3 and strictness >= 3: return -1
		if strict_min <= 4 and strictness >= 4: return -1
		if strict_min <= 5 and strictness >= 5: return -1
		if strict_min <= 6 and strictness >= 6: return -1
		
		# We failed
		return -1
	
	def match_number(self, the_line):
		"""Finds a number within the line"""
		results = re.search(r'\b(-?[0-9\.]+)\b', the_line.replace(",", ""))
		
		if results == None: return 0
		results = results.groups()[0].strip()
		
		return int(results)
	
	def match_int(self, the_line):
		"""Specifically finds a whole number in the line"""
		results = re.search(r'\b(-?[0-9]+)\b', the_line.replace(",", ""))
		
		if results == None: return 0
		results = results.groups()[0].strip()
		
		return int(results)
	
	def find_key(self, the_key, the_dict):
		"""Performs a case-insensetive search for a key in a dictionary"""
		the_key = the_key.lower()
		for k in the_dict.keys():
			if k.lower() == the_key:
				return k
		
		return None
	
	def find_in_list(self, the_key, the_list):
		"""Performs a case-insensetive search for a key in a dictionary"""
		the_key = the_key.lower()
		for k in the_list:
			if k.lower() == the_key:
				return the_list.index(k)
		
		return None
	
class Order_post (database.DB_connected_object):
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
	
	def __init__(self, row = {}):
		super(Order_post, self).__init__(row)
		
		self.blocks = []
		
		self.time_taken = []
		self.total_time = 0
		
		self.team_ref = None
	
	def prep_for_split(self, content):
		"""We take in the post and create a list of blocks"""
		# Some regex patterns for later
		colour_match		= r'(#[a-fA-Z0-9]{1,6}|[a-zA-Z]{1,9})'
		headers_to_ignore	= r'(General orders|Specific orders|([a-zA-Z0-9\' ])*? ?Turn ?[0-9]{1,3} ?(Orders)?)'
		
		# Not sure why this is in rob1
		# $totalPost	= str_replace(':', '', $post);
		
		# Remove irrelevant titles
		content = re.sub(r'\[(o|b|title|h[1-5])\]%s\[\/(o|b|title|h[1-5])\]' % headers_to_ignore, '', content)
		
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
		content = re.sub(r'\[size=([0-9]{1,4})\](.*?)\[/size\]', r'\2', content)
		
		# Get rid of boxes, they don't help us work out the title
		content = re.sub(r'\[(box|fullbox)=(%s)(,%s)?\](.*?)\[/\1]' % (colour_match, colour_match), r'\6', content)
		
		# Quotes too, they're not helpful for title calculation
		content = re.sub(r'\[quote(="([^"]*?)")?\](.*?)\[/quote\]', r'\3', content)
		
		content = re.sub(r'<!-- l --><a class="postlink-local" href="([^"]*)">([^<]*)</a><!-- l -->', r'\2 (\1)', content)
		
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
		
		title_type			= ''
		title_name			= ''
		order_start_line	= -1
		ordrer_end_line		= -1
		
		for l in range(line_count):
			# Human line count is l + 1
			the_line = the_post[l].strip()
			
			# Skip empty lines
			if the_line == "":
				continue
			
			# Search for an order title here
			title_search = re.search(r'^\[(o|b|u|title|h[1-5])\](.*?)\[\/(\1)\]', the_line)
			
			# No results found
			if title_search == None:
				continue
			
			title_type = title_search.groups()[0]
			title_name = title_search.groups()[1]
			order_start_line = l
			order_end_line = 999999
			
			find = r'^\[(%s)\](.*?)\[\/(%s)\]' % (title_type, title_type)
			
			for sub_l in range(l+1, line_count):
				temp_line = the_post[sub_l].strip()
				# This was all commented out in Rob1, not sure why...
				# $find		= '/[0-9\\.]{1,9} ?Materials/i';
				# $tempLine	= preg_replace($find, '', $tempLine);
				# 		
				# $tempLine	= str_ireplace('[i][/i]', '', $tempLine);
				# $tempLine	= str_ireplace('[b][/b]', '', $tempLine);
				# $tempLine	= str_ireplace('[o][/o]', '', $tempLine);
				# $tempLine	= str_ireplace('[title][/title]', '', $tempLine);
				# $tempLine	= str_ireplace('[u][/u]', '', $tempLine);
				# 		
				# $tempLine = trim($tempLine);
				
				results = re.findall(find, temp_line)
				
				if len(results) > 0:
					order_end_line = sub_l
					break
			
			blocks.append(Order_block(team=self.team))
			blocks[-1].title_name	= title_name
			blocks[-1].content		= "\n".join(the_post[order_start_line+1:order_end_line])
			blocks[-1].team_ref		= self.team_ref
		
		self.blocks.extend(blocks)
		
	
	def match(self, ignore=[]):
		"""Match each of self.blocks"""
		total_start_time = time.time()
		
		for b in self.blocks:
			start_time = time.time()
			block_type = b.get_type()
			
			if block_type in ignore: continue
			
			if		block_type == 'construction':	construction_orders.run(b)
			elif	block_type == 'military':		military_orders.run(b)
			elif	block_type == 'diplomacy':		diplomacy_orders.run(b)
			elif	block_type == 'research':		research_orders.run(b)
			elif	block_type == 'operatives':		operative_orders.run(b)
			elif	block_type == 'mages':			mage_orders.run(b)
			elif	block_type == 'trades':			trade_orders.run(b)
			elif	block_type == 'enchantment':	enchantment_orders.run(b)
			elif	block_type == 'relocation':		relocation_orders.run(b)
			elif	block_type == 'chosen':			chosen_orders.run(b)
			elif	block_type == 'migration':		migration_orders.run(b)
			elif	block_type == 'founding':		founding_orders.run(b)
			elif	block_type == 'disband':		disbanding_orders.run(b)
			elif	block_type == 'command':		command_orders.run(b)
			elif	block_type == 'unknown':		unknown_orders.run(b)
			
			else:
				e = Exception("Error in orders.order_utilities.match_block: No handler for type '%s'" % block_type)
				raise e
			
			self.time_taken.append('%s: %s' % (b.title_name, round(time.time() - start_time, 2)))
		
		self.total_time = round(time.time() - total_start_time,2)
	
