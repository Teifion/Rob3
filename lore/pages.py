# from lore import buildings, history, deities, irs, magic, monsters, techs
from pages import common
import lore
import re
import json
from io import StringIO
from queries import lore_q
from data_classes import lore_entry

def _filter(cursor, category, page, level, filter_list):
	le = lore_q.get_one_entry(cursor, category, page)
	
	if le == None: return None
	
	le.get_blocks(cursor)
	
	return le.filter(cursor, level, filter_list)

formatting_patterns = (
	# MATCH												BBCODE				PLAIN
	(re.compile(r'<strong>(.*?)</strong>'),				r'[b]\1[/b]',		r'\1'),
	(re.compile(r'<ul>(.*?)</ul>'),						r'[list]\1[/list]',	r'\1'),
	(re.compile(r'<li>(.*?)</li>'),						r'[*]\1',			r' - \1'),
	(re.compile(r'<span class="stitle">(.*?)</span>'),	r'[o]\1[/o]',		r'\1'),
	(re.compile(r'<!--.*?-->', re.DOTALL),				r'',				r''),
)

def convert(blocks, mode):
	# text = "<br /><br />".join([b['description'] for b in blocks])
	textl = []
	for b in blocks:
		if b.get("title", "") == "": b['title'] = b.get('name', "").capitalize()
		textl.append('<span class="stitle">{0}</span><br />'.format(b['title']))
		textl.append(b['description'])
		textl.append("<br /><br />")
	
	text = "".join(textl)
	
	text = text.replace("\t", "")
	text = text.replace("\n", "")
	text = text.replace("<br />", "\n")
	
	if mode == "bbcode":
		for regex, replacement, dud in formatting_patterns:
			text = regex.sub(replacement, text)
	elif mode == "plaintext":
		for regex, dud, replacement in formatting_patterns:
			text = regex.sub(replacement, text)
	
	return text.strip()

def get_bbcode(cursor, category, page, level = "public", filter_list = []):
	level = lore_entry.levels.index(level)
	data = _filter(cursor, category, page, level, filter_list)
	
	if data == None:
		return "%s.%s not found" % (category, page)
	
	return convert(data, "bbcode")

def get_html(cursor, category, page, level = "public", filter_list = []):
	level = lore_entry.levels.index(level)
	data = _filter(cursor, category, page, level, filter_list)
	
	if data == None:
		raise KeyError("%s.%s not found" % (category, page))
		return "%s.%s not found" % (category, page)
	
	output = []
	for i, t in enumerate(data):
		if t["title"] != "":
			if i == 0:
				tag = 1
			else:
				tag = 4
			
			output.append('<h%d><a href="#%s" id="%s">%s</a></h%d>' % (
				tag,
				common.js_name(t['title']),
				common.js_name(t['title']),
				t['title'],
				tag,
			))
			
		output.append(t['description'].replace("<tab>", "&nbsp;&nbsp;&nbsp;&nbsp;"))
		
		if not t.get('no_break', False):
			output.append("<br /><br />")
	
	return "\n".join(output)

def get_plaintext(cursor, category, page, level = "public", filter_list = []):
	level = lore_entry.levels.index(level)
	data = _filter(cursor, category, page, level, filter_list)
	
	if data == None:
		return "%s.%s not found" % (category, page)
	
	return convert(data, "plaintext")

