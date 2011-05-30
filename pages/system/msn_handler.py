from queries import player_q
from pages import common
import re

from functions import request_f, player_f

page_data = {
	"Title":	"MSN Handler",
	"Admin":	True,
	"Header":	False,
}

def msn_auth_needed():
	return "You have not registered your MSN name to a team, to do this send 'addme <name>' where <name> is your forum name. Teifion will need to manually approve it before it is added."

def run_requests(cursor, email, the_player, args):
	if the_player == None: return msn_auth_needed()
	
	return request_f.msn_run_orders(cursor, the_player.team)

def msn_help(cursor, email, the_player, args):
	return "This function is not written yet"

def hello(cursor, email, the_player, args):
	return "Hello there, I'm Rob 3"

def add_request(cursor, email, the_player, args):
	if the_player != None:
		return "You have already been added, %s" % the_player.name
	
	player_name = " ".join(args)
	return player_f.add_msn_request(cursor, player_name, email)

function_dict = {
	'?':				hello,
	'hello':			hello,
	'hi':				hello,
	'yo':				hello,
	# 'boring':			gibberish(),
	'help':				msn_help,
	
	# Player stuff
	# if cmd == 'whoami':			return whoami(email)
	# if cmd == 'whoami':			return "Sorry but that command is disabled"
	# if cmd == 'mystats':		return myStats(email)
	# if cmd == 'myfeats':		return myFeats(email)
	# if cmd == 'mydeaths':		return myDeaths(email)
	# if cmd == 'mykills':		return myKills(email)
	# if cmd == 'buyfeat':		return buyFeat(email, args)
	
	# Misc
	# if cmd == 'currentturn':	return common.current_turn()
	# if cmd == 'current_turn':	return common.current_turn()
	# if cmd == 'time':			return theTime()
	# if cmd == 'find':			return find(args)
	
	# Utilities
	# if cmd == 'list':			return find(args)
	# if cmd == 'show':			return find(args)
	# if cmd == 'path':			return find_path(args, move_speed="Marching", move_type="Generic path")
	# if cmd == 'path_infantry':	return find_path(args, move_speed="Marching", move_type="Medium foot")
	# if cmd == 'path_cavalry':	return find_path(args, move_speed="Riding", move_type="Medium cav")
	# if cmd == 'path_ships':		return find_path(args, move_speed="Sailing", move_type="Sail")
	# if cmd == 'path_ship':		return find_path(args, move_speed="Sailing", move_type="Sail")
	# if cmd == 'path_airship':	return find_path(args, move_speed="Sailing", move_type="Air")
	# if cmd == 'path_balloon':	return find_path(args, move_speed="Sailing", move_type="Air")
	
	# path_infantry, path_cavalry, path_ship
	# if cmd == 'map':			return mapLink()
	# if cmd == 'how long':		return "%s" % (holder.status)
	# if cmd == 'eta':			return "%s" % (holder.status)
	# # if cmd == 'makemap':		return makeMap(email)
	# if cmd == 'roll':			return roll(args)
	
	# Links
	# if cmd == 'to':				return "http://woarl.com/to"
	# if cmd == 'addme':			return add_msn(email, args)
	# if cmd == 'links':			return links(email)
	
	# Team stuff
	"requests":				run_requests,
	
	"addme":				add_request,
	# if cmd == 'citydesc':		return cityDesc(email, args)
	
	# Admin stuff
	# if email == 'citizen@woarl.com':
	# 	if cmd == 'listU':		return getList()
	# 	if cmd == 'twitter' or cmd == "tweet":	return tweet(args)
	# 	if cmd == "follow":		return follow(args)
	# 	if cmd == "unfollow":	return unfollow(args)
	# 	if cmd == '!status':
	# 		holder.status = "Status not set"
	# 		return "\n"
	
	# if cmd == 'status':			return "http://twitter.com/woarl"
	
	# Stuff with more than one
	# args = args.strip().split(" ")
	
	
	# lowerMessage = message.lower().strip()
	
	# if lowerMessage == "dude, you're awesome":		return "Cheers"
	# if lowerMessage == "dude, you are awesome":		return "Cheers"
	# if lowerMessage == "dude, youre awesome":		return "Cheers"
	# 
	# if lowerMessage == "you're gay":		return "No I'm not, you are"
	# if lowerMessage == "youre gay":			return "No I'm not, you are"
	# if lowerMessage == "you are gay":		return "No I'm not, you are"
	# 
	# if lowerMessage == "you smell":			return "Not as badly as you"
	# if lowerMessage == "tei smells":		return "Not as badly as you"
	# if lowerMessage == "teif smells":		return "Not as badly as you"
	# if lowerMessage == "teifion smells":	return "Not as badly as you"
	# 
	# if lowerMessage == "do it, bitch":		return "Make me"
	# if lowerMessage == "do it bitch":		return "Make me"
	# 
	# if lowerMessage == "thank you":			return "You're welcome"
	# if lowerMessage == "thankyou":			return "You're welcome"
	# if lowerMessage == "thanks":			return "You're welcome"
	# 
	# if lowerMessage == "excellent":			return "Good to hear"
	# if lowerMessage == "sorry":				return "That's okay"
	# 
	# if lowerMessage == "bye":				return "Bye"
	# if lowerMessage == "bye bye":			return "Bye"
	# if lowerMessage == "godo bye":			return "Bye"
	# if lowerMessage == "buh bye":			return "Bye"
	# if lowerMessage == "b bye":				return "Bye"
	# 
	# if lowerMessage == "good night":		return "Good night"
	
	# return """I'm sorry but that command was not recognised, try typing "help" for a list of commands."""
}

def main(cursor):
	content = common.get_val('content')
	email = common.get_val('email')
	
	the_player = player_q.get_player_by_msn(cursor, email)
	
	words = re.split(r'\s+', content)
	
	cmd = words[0].lower()
	del(words[0])
	if cmd in function_dict:
		return function_dict[cmd](cursor, email, the_player, words)
	else:
		# Nothing found
		return ""
		