import urllib.request
import re
from hashlib import md5
from functions import cli_f, team_f
from pages import common
from queries import campaign_q, battle_q
from classes import voi

# Importing of pages
import pages.war.list_campaigns
import pages.war.setup_campaign
import pages.war.perform_battle
import pages.war.perform_by_army
import pages.war.setup_battle
import pages.war.list_battles

modes = {
	"list_campaigns":	pages.war.list_campaigns,
	"setup_campaign":	pages.war.setup_campaign,
	"perform_battle":	pages.war.perform_battle,
	"perform_by_army":	pages.war.perform_by_army,
	"setup_battle":		pages.war.setup_battle,
	"list_battles":		pages.war.list_battles,
}


def turn_key(turn=-1):
	if turn < 1: turn = common.current_turn()
	
	m = md5()
	m.update("GM_turn_key".encode("utf-8"))
	m.update(str(turn).encode("utf-8"))
	return m.hexdigest()

# It'll be used a lot, might as well cache and shorthand it at the same time
tk = turn_key()


regexes = {
	"forms":			re.compile(r"<form .*?</form>", re.DOTALL),
	"marked_comments":	re.compile(r"<!-- PY -->.*?<!-- PYEND -->", re.DOTALL),
	"comments":			re.compile(r"<!--.*?-->", re.DOTALL),
	
	# List campaigns
	"links": (
		(re.compile(r"web.py\?mode=list_campaigns&amp;turn=([0-9]*)"), 'http://woarl.com/board/viewtopic.php?f=10&amp;t=%d' % voi.gm_topic_id),
		(re.compile(r"web.py\?mode=setup_campaign&amp;campaign=([0-9]*)"), r'%s_\1_setup_campaign.html' % (tk)),
		(re.compile(r"web.py\?mode=list_battles&amp;campaign=([0-9]*)"), r'%s_\1_list_battles.html' % (tk)),
		(re.compile(r"web.py\?mode=perform_battle&amp;battle=([0-9]*)"), r'%s_\1_perform_battle.html' % (tk)),
		(re.compile(r"web.py\?mode=perform_by_army&amp;battle=([0-9]*)"), r'%s_\1_perform_by_army.html' % (tk)),
		(re.compile(r"web.py\?mode=setup_battle&amp;battle=([0-9]*)"), r'%s_\1_setup_battle.html' % (tk)),
	),
}

def get_page(cursor, mode, **kwargs):
	res = modes[mode].main(cursor, **kwargs)
	res = regexes['marked_comments'].sub("", res)
	res = regexes['forms'].sub("", res)
	# res = regexes['comments'].sub("", res)
	
	for find, replace in regexes['links']:
		res = find.sub(replace, res)
	
	return res

def combine_dicts(a, b):
	res = dict(a)
	for k, v in b.items():
		if k in res:
			res[k] += v
		else:
			res[k] = v
	return res
	

def build_turn(w, turn=-1):
	"""Build a list of files to upload for the current turn based on campaigns etc"""
	
	if turn < 1:
		turn = common.current_turn()
	
	files = {}
	
	# Update topic
	update_topic_new(w)
	update_topic_old(w)
	
	# Save it
	with open('%s%d_overview.html' % (common.data['cache_path'], turn), 'w') as f:
		f.write(voi.headers.format(title = "Turn %d campaign overview" % turn))
		f.write(get_page(w.cursor, "list_campaigns", turn = turn))
		f.write(voi.footers)
		f.write(cli_f.padding)
		
		files['%s_%d_overview.html' % (tk, turn)] = '%s%d_overview.html' % (common.data['cache_path'], turn)
	
	# For each campaign
	for c in w.campaigns_from_turn(turn=turn):
		files = combine_dicts(files, _build_campaign(w, c))
	
	return files

def _build_campaign(w, campaign):
	files = {}
	camp = w.campaigns()[campaign]
	
	# Setup campaign
	with open('%s%d_setup_campaign.html' % (common.data['cache_path'], camp.id), 'w') as f:
		f.write(voi.headers.format(title = "Setup campaign %s" % camp.name))
		f.write(get_page(w.cursor, "setup_campaign", campaign_id = camp.id))
		f.write(voi.footers)
		f.write(cli_f.padding)
		
		files['%s_%d_setup_campaign.html' % (tk, camp.id)] = '%s%d_setup_campaign.html' % (common.data['cache_path'], camp.id)
	
	with open('%s%d_list_battles.html' % (common.data['cache_path'], camp.id), 'w') as f:
		f.write(voi.headers.format(title = "Battle list for %s" % camp.name))
		f.write(get_page(w.cursor, "list_battles", campaign_id = camp.id))
		f.write(voi.footers)
		f.write(cli_f.padding)
		
		files['%s_%d_list_battles.html' % (tk, camp.id)] = '%s%d_list_battles.html' % (common.data['cache_path'], camp.id)
		# return files
	
	for b in w.battles_from_campaign(camp.id):
		files = combine_dicts(files, _build_battle(w, b))
	
	return files

def _build_battle(w, battle):
	files = {}
	battle = w.battles()[battle]
	
	# Perform battle
	with open('%s%d_perform_battle.html' % (common.data['cache_path'], battle.id), 'w') as f:
		f.write(voi.headers.format(title = "Perform battle %s" % battle.name))
		f.write(get_page(w.cursor, "perform_battle", battle_id = battle.id))
		f.write(voi.footers)
		f.write(cli_f.padding)
		
		files['%s_%d_perform_battle.html' % (tk, battle.id)] = '%s%d_perform_battle.html' % (common.data['cache_path'], battle.id)
	
	with open('%s%d_perform_by_army.html' % (common.data['cache_path'], battle.id), 'w') as f:
		f.write(voi.headers.format(title = "Perform by army %s" % battle.name))
		f.write(get_page(w.cursor, "perform_by_army", battle_id = battle.id))
		f.write(voi.footers)
		f.write(cli_f.padding)
		
		files['%s_%d_perform_by_army.html' % (tk, battle.id)] = '%s%d_perform_by_army.html' % (common.data['cache_path'], battle.id)
	
	# Setup battle
	with open('%s%d_setup_battle.html' % (common.data['cache_path'], battle.id), 'w') as f:
		f.write(voi.headers.format(title = "Setup battle %s" % battle.name))
		f.write(get_page(w.cursor, "setup_battle", battle_id = battle.id))
		f.write(voi.footers)
		f.write(cli_f.padding)
		
		files['%s_%d_setup_battle.html' % (tk, battle.id)] = '%s%d_setup_battle.html' % (common.data['cache_path'], battle.id)
	
	
	return files

def build_campaign(w, campaign):
	campaign = campaign_q.get_one_campaign(w.cursor, campaign)
	
	# f = _build_campaign(w, campaign.id)
	# for k, v in f.items():
	# 	print(k, v)
	
	return _build_campaign(w, campaign.id)

def build_battle(w, battle):
	battle = battle_q.get_one_battle(w.cursor, battle)
	return _build_battle(w, battle.id)

def update_topic_new(w):
	output = ["[o]Campaigns[/o]\n"]
	
	for c in w.campaigns_from_turn(turn=common.current_turn()):
		output.append("[url=http://woarl.com/voi/%s_%d_list_battles.html]%s[/url] - " % (tk, c, w.campaigns()[c].name))
		output.append("[url=http://woarl.com/voi/%s_%d_setup_campaign.html]setup[/url]" % (tk, c))
		output.append("\n")
	
	output.append("\n[o]Teams[/o]\n")
	for t, the_team in w.active_teams().items():
		if the_team.ir: continue
		team_hash = team_f.team_hash(the_team.name)
		output.append("[url=http://woarl.com/board/viewforum.php?f=%d]%s[/url] - " % (the_team.forum_url_id, the_team.name))
		output.append("[url=http://woarl.com/ti/%s.html]Team Info[/url] - " % (team_hash))
		output.append("[url=http://woarl.com/board/viewtopic.php?t=%d.html]Orders[/url]" % (the_team.intorders_topic))
		output.append("\n")
	
	output = "".join(output)
	getter_data = "p=%s&mode=postUpdate&post=%d&string=%s" % (common.data['getterPass'], voi.current_turn_post, output)
	result = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()

def update_topic_old(w):
	output = ["[o]Campaigns[/o]\n"]
	
	for c in w.campaigns_from_turn(turn=common.current_turn()):
		output.append("[url=http://woarl.com/voi/%s_%d_list_battles.html]%s[/url] - " % (tk, c, w.campaigns()[c].name))
		output.append("[url=http://woarl.com/voi/%s_%d_setup_campaign.html]setup[/url]" % (tk, c))
		output.append("\n")
	
	output.append("\n[o]Teams[/o]\n")
	for t, the_team in w.active_teams().items():
		if the_team.ir: continue
		team_hash = team_f.team_hash(the_team.name)
		output.append("[url=http://woarl.com/board/viewforum.php?f=%d]%s[/url] - " % (the_team.forum_url_id, the_team.name))
		output.append("[url=http://woarl.com/ti/%s.html]Team Info[/url] - " % (team_hash))
		output.append("[url=http://woarl.com/board/viewtopic.php?t=%d.html]Orders[/url]" % (the_team.intorders_topic))
		output.append("\n")
	
	output = "".join(output)
	getter_data = "p=%s&mode=postUpdate&post=%d&string=%s" % (common.data['getterPass'], voi.current_turn_post, output)
	result = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()