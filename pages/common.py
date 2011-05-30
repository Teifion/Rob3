# -*- coding: utf-8 -*-

import database
import re
from functions import team_f
import random

import cgi
cgi_form = cgi.FieldStorage()

data = {
	'current_turn':	None,
	'mode':			'',
	'getter_url':	'GETTER URL',
	'getterPass':	'PASSWORD',
	# "file_path":	'/Users/teifion/programming/python/rob3/',
	'board_url':	'http://woarl.com/board/',
	'server_path':	'http://localhost/rob3/',
	'rob_url':		'http://localhost/rob3/web.py',
	'woa_folder':	"/Library/WebServer/Documents/woa",
	'cache_path':	'/Library/WebServer/CGI-Executables/rob3/cache/',
	'rob_site':		'/Library/WebServer/Documents/rob_site',
	'media_path':	'media/',
	'remote_media':	'http://woarl.com/images/',
	'server_fpath':	'/Library/WebServer/CGI-Executables/rob3',# same thing but for files
	'rob_fpath':	'/Library/WebServer/Documents/rob3',
	'analytics':	"",
	'analytics2':	'''<script type="text/javascript">
		var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
		document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
		</script>
		<script type="text/javascript">
		try {
		var pageTracker = _gat._getTracker("ANALYTICS");
		pageTracker._trackPageview();
		} catch(err) {}</script>''',
	
	'double_click_id_cache':	0,
	
	'uid':					str(random.random())[3:9],
	# 'system_path':		"/Library/WebServer/CGI-Executables/rob3",
	# 'web_url':			"http://localhost/cgi-bin/rob3/web.py",
}

# def number_format (n):
# 	"""Adds commas to a number"""
# 	
# 	if n < 0: return '-' + number_format(-n) 
# 	if n < 1000: return str(n) 
# 	return '%s,%03d' % (number_format(n//1000), n%1000)

def number_format (n):
	return format(n, ',')

def approx(n):
	if n < 1000:		return 'Less than 1,000'
	if n < 10000:		return 'Approx %s' % number_format(int(round(n, -3)))
	if n < 100000:		return 'Approx %s' % number_format(int(round(n, -4)))
	if n < 1000000:		return 'Approx %s' % number_format(int(round(n, -4)))
	if n < 10000000:	return 'Approx %s' % number_format(int(round(n, -5)))
	if n < 100000000:	return 'Approx %s' % number_format(int(round(n, -6)))

# Used to return a number
def napprox(n):
	if n < 1000:		return 1000
	if n < 10000:		return int(round(n, -3))
	if n < 100000:		return int(round(n, -4))
	if n < 1000000:		return int(round(n, -4))
	if n < 10000000:	return int(round(n, -5))
	if n < 100000000:	return int(round(n, -6))


def check_box(name, checked=False, custom_id=''):
	output = ['<input type="checkbox" name="%s" value="True"' % name]
	
	if checked:
		output.append('checked="checked"')
	
	if custom_id != '':	output.append('id="%s"' % custom_id)
	else:				output.append('id="%s"' % name)
	
	output.append('/>')
	return " ".join(output)

def text_box(name, text='', size=15, tabIndex=-1, onchange='', custom_id='<>', style="", warn_on = None):
	if custom_id == "<>": custom_id = name
	
	if warn_on != None:
		if warn_on(text):
			style = "%sbackground-color:#FAA;border:2px solid #A00;" % style
	
	output = ['<input type="text" name="%s" size="%s" value="%s" onchange="%s" id="%s" style="%s"' % (name, size, text, onchange, custom_id, style)]
	
	if tabIndex > 0: output.append('tabIndex="%s"' % tabIndex)
	
	output.append(">")
	return " ".join(output)

def option_box(name, elements = {}, element_order = [], tab_index = -1, onchange="", custom_id = "<>", selected=""):
	disabled_count = 0
	if custom_id == "<>": custom_id = name
	
	output = ['<select name="%s" id="%s" onchange="%s"' % (name, custom_id, onchange)]
	
	if tab_index > 0:
		output.append('tabIndex="%s"' % tab_index)
	
	output.append('>')
	
	if elements.__class__ == list or elements.__class__ == tuple:
		for i, e in enumerate(elements):
		# for i in range(0, len(elements)):
		# 	e = elements[i]
			is_selected = ""
			if selected == e: is_selected = "selected='selected'"
			
			output.append('<option value="%s" %s>%s</option>' % (i, is_selected, e))
			
	elif element_order != []:
		for e in element_order:
			is_selected = ""
			if selected == e: is_selected = "selected='selected'"
			
			if e == "disabled":
				disabled_count += 1
				output.append('<option value="disabled_%s" disabled="disabled">&nbsp;</option>' % disabled_count)
				continue
			
			output.append('<option value="%s" %s>%s</option>' % (e, is_selected, elements[e]))
	
	output.append('</select>')
	return "".join(output)

def get_val(value_name, default = ''):
	for http_data in cgi_form.list:
		if http_data.name == value_name:
			return http_data.value
	
	return default

def print_post_data():
	output = []
	
	for http_data in cgi_form.list:
		output.append("%s = %s" % (http_data.name, http_data.value))
		
	return "<br />".join(output)

def current_turn(force_requery=False):
	if not force_requery:
		if data['current_turn'] != None: return data['current_turn']
	
	cur = database.get_cursor(True)
	query = "SELECT turn FROM turns ORDER BY turn DESC LIMIT 1 OFFSET 1;"
	try: cur.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cur:
		data['current_turn'] = row['turn']
		return row['turn']

def redirect(new_location, delay = 0):
	"""Performs a JS redirect to the new location, delay in milliseconds"""
	
	if delay > 0:
		return """
		<script type="text/javascript" charset="utf-8">
			setTimeout("document.location='%s';", %s);
		</script>""" % (new_location, delay)
	else:
		return """
		<script type="text/javascript" charset="utf-8">
			setTimeout("document.location='%s';");
		</script>""" % (new_location)
	
def select_team_form(cursor, target_mode, **form_values):
	"""Returns a form for selecting a team"""
	
	hidden_values = []
	for k, v in form_values.items():
		hidden_values.append('<input type="hidden" name="%s" value="%s" />' % (k, v))
	
	output = """
	<form id="select_team_form" action="web.py" method="get" accept-charset="utf-8" style="width: 250px;">
		<input type="hidden" name="mode" id="mode" value="%s" />
		%s
		%s
		<!--
		<a class="block_link" href="#" onclick="$('#select_team_form').submit(); return false;">Choose team</a>
		-->
		<input type="submit" value="Choose team" />
	</form>
	""" % (target_mode, team_f.structured_list(cursor, field_id="select_team_input"), "".join(hidden_values))
	
	return output

def bstr(binput):
	return ('True','')[not binput]

bbcode_patterns = (
	(re.compile(r"\[url=(http://.*?)\](.*?)\[/url\]"), r'<a href="\1">\2</a>'),
	(re.compile(r"\[url=(.*?)\](.*?)\[/url\]"), r'<a href="\1">\2</a>'),
	(re.compile(r"\[url](.*?)\[/url\]"), r'<a href="\1">\1</a>'),
	
	# Titles
	(re.compile(r"\[title\](.*?)\[/title\]"), r'<span class="stitle">\1</span>'),
	(re.compile(r"\[o\](.*?)\[/o\]"), r'<span class="stitle">\1</span>'),
	
	# Common tags
	(re.compile(r"\[b\](.*?)\[/b\]"), r"<strong>\1</strong>"),
	(re.compile(r"\[i\](.*?)\[/i\]"), r"<em>\1</em>"),
	(re.compile(r"\[u\](.*?)\[/u\]"), r"<u>\1</u>"),
	(re.compile(r"\[sub\](.*?)\[/sub\]"), r"<sub>\1</sub>"),
	(re.compile(r"\[sup\](.*?)\[/sup\]"), r"<sup>\1</sup>"),
	
	# Pos, Neg
	(re.compile(r"\[pos\](.*?)\[/pos\]"), r'<span class="pos">\1</span>'),
	(re.compile(r"\[neg\](.*?)\[/neg\]"), r'<span class="neg">\1</span>'),
	
	# H1-5
	(re.compile(r"\[h([1-5])\](.*?)\[/h\1\]"), r"<h\1>\2</h\1>"),
	
	# Size
	(re.compile(r"\[size=([0-9]{1,4})\](.*?)(\[/size\])"), r'<span style="font-size: \1%%">\2</span>'),
	
	# Color
	(re.compile(r"\[color=(.*?)\](.*?)(\[/color\])"), r'<span style="color: \1">\2</span>'),
	
	# IR boxes
	(re.compile(r'\[ir\](.*?)(\[/ir\])'), r'<div class="ir_box">\1</div>'),
	
	# Fullbox
	(re.compile(r"\[fullbox=(#[0-9A-Fa-f]{3,6}),(#[0-9A-Fa-f]{3,6})\](.*?)(\[/fullbox\])"),
		r'<div style="background-color: \1; border: 1px solid \2; padding: 5px; margin: 5px;">\3</div>'),
	
	# Box
	(re.compile(r'\[box=(#[0-9A-Fa-f]{3,6})\](.*?)(\[/box\])'),
		r'<div style="background-color: \1; padding: 5px; margin: 5px;">\2</div>'),
	
	# Box with colour
	(re.compile(r"\[box=([^\]]*)\](.*?)(\[/box\])"),
		r'<div style="background-color: \1; padding: 5px; margin: 5px;">\2</div>'),
	
	# Quotebox
	(re.compile(r'\[quote\](.*?)\[/quote\]'),
		r'<div style="background-color: #FFD; border: 1px solid #880; padding: 5px; margin: 5px;"><strong>Quote:</strong>\1</div>'),
	
	# Img
	(re.compile(r'\[img\](.*?)\[/img\]'),
		r'<a href="\1"><img style="max-width:600px; max-height:600px;" src="\1" /></a>'),
	
	# Rob
	(re.compile(r'\[rob\](.*?)\[/rob\]'),
		r'<div style="background-color: #EEE; border: 1px dotted #000; padding: 5px; margin: 5px;">\1</div>'),
	
	# Smilies
	(re.compile(r'{SMILIES_PATH}'),
		r'http://woarl.com/board/images/smilies'),
)
def bbcode_to_html(text):
	text = text.replace("\n", "<br />")
	
	for regex, replacement in bbcode_patterns:
		text = regex.sub(replacement, text)
	
	text = text.replace("[t][/t]", '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
	return text

html_to_terminal_patterns = (
	# Neg
	(re.compile(r"\<span class='neg'>(.*?)</span>"), '\033[31m\\1\033[30;0m'),
	
	# Pos
	(re.compile(r"\<span class='pos'>(.*?)</span>"), '\033[32m\\1\033[30;0m'),
)
def html_to_terminal(text):
	text = text.replace("\n", "<br />")
	
	for regex, replacement in html_to_terminal_patterns:
		text = regex.sub(replacement, text)
	
	text = text.replace("[t][/t]", '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
	return text

def clean_name(text):
	"""A name without quote characters"""
	return text.replace("'", "").replace('"', "")

def js_name(text):
	# text = text.replace(" ", "")# A JS name does not need the spaces removed
	return text.replace("'", "\\'").replace("(", "").replace(")", "")
	# return text.replace("'", "").replace('"', "").replace(" ", "_")

def onload(javascript, remote=False):
	"""Creates a small image that when loaded will run JS"""
	if not remote:
		return '''<img src="%simages/grid_25.png" width="0" height="0" onload="%s">''' % (data['media_path'], javascript)
	else:
		return '''<img src="%simages/grid_25.png" width="0" height="0" onload="%s">''' % (data['remote_media'], javascript)

def doubleclick_text(table, field, where_id, value, label_style="", size=10):
	return doubleclick_text_full(table, field, "id=%d" % int(where_id), value, label_style, size)

def doubleclick_text_full(table, field, where_field, value, label_style="", size=10):
	"""Creates a label that when double clicked turns into a textbox, when the textbox loses focus, it saves itself"""
	data['double_click_id_cache'] += 1
	
	# If no value is sent we want something to click on
	if value == "":
		value = "&nbsp;&nbsp;&nbsp;"
	
	return """<span style="%(label_style)s" id="%(label)s" ondblclick="$('#%(input)s').val($('#%(label)s').text()); $('#%(label)s').hide(); $('#%(input)s').show(); $('#%(input)s').select();">%(value)s</span>
		<input style="display:none; margin:-2px;" type="text" name="value" id="%(input)s" size="%(size)s" value="" onblur="$('#%(label)s').load('web.py', {'mode':'edit_one_field','table':'%(table)s','field':'%(field)s','where':'%(where)s','value':$('#%(input)s').val()}, function () {$('#%(label)s').show(); $('#%(input)s').hide();});" />""" % {
	"table": table,
	"field": field,
	"where": where_field,
	"value": value,
	"label_style": label_style,
	"size": size,
	
	"label": "label_%s_%s_%s" % (field, data['double_click_id_cache'], data['uid']),
	"input": "input_%s_%s_%s" % (field, data['double_click_id_cache'], data['uid']),
	}

def headers(title_name, css="", javascript="", local_path=False, js_libs=[], tiers=1, content_div=True):
	# Makes printing those flashy links that much easier
	def linkfade(link_name):
		return '''class="clear_link" onmouseover="$('#%sLinkInfo').fadeIn(250);" onmouseout="$('#%sLinkInfo').fadeOut(250);"''' % (link_name, link_name)
	
	str_tier = "".join(["../" for i in range(tiers)])
	
	jquery_path = "%sincludes/jquery.js" % str_tier
	jqueryui_path = "%sincludes/jquery-ui.js" % str_tier
	css_path	= "%sstyles.css" % str_tier
	if local_path:
		jquery_path = '%sjquery-1.3.2.min.js' % data['media_path']
		jquery_path = '%sjquery.js' % data['media_path']
		jqueryui_path = '%sjquery-ui.js' % data['media_path']
		css_path	= "http://localhost/woa/styles.css"
		
	
	js_lib_s = "".join(['<script type="text/javascript" charset="utf-8" src="%s"></script>' % j for j in js_libs])
	
	if content_div:
		content_div = '''<!-- 852px width normally, 20px padding -->
		<div class="contentWide" style="padding: 0px; width: 892px;">'''
	else:
		content_div = ''
	
	
	return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<title>%(title_name)s</title>
		<script type="text/javascript" src="%(jquery_path)s" charset="utf-8"></script>
		<!--<script type="text/javascript" src="%(jqueryui_path)s" charset="utf-8"></script>-->
		<link rel="stylesheet" href="%(css_path)s" type="text/css" media="screen" title="no title" charset="utf-8" />%(js_lib)s
		<script type="text/javascript" charset="utf-8">
			%(javascript)s
		</script>
		<style type="text/css" media="screen">
			%(css)s
		</style>
	</head>
	<body id="body">
		<div class="page">
			<div class="header">
			<div id="logo">
				<a id="woaLogo" href="../"></a>
			</div>
			<ul>
				<li id="registerLink"><a href="http://woarl.com/board/ucp.php?mode=register" %(linkfade_register)s>Register</a></li>
				<li id="loginLink"><a href="http://woarl.com/board/ucp.php?mode=login" %(linkfade_login)s>Login</a></li>
				<li id="contactLink"><a href="../pages/general/contact.html" %(linkfade_contact)s>Contact</a></li>
				<li id="aboutLink"><a href="../pages/general/about.html" %(linkfade_about)s>About</a></li>
				<li id="blogLink"><a href="http://woarl.com/blog/" %(linkfade_blog)s>Blog</a></li>
				<li id="guideLink"><a href="../pages/general/starting.html" %(linkfade_guide)s>Guide</a></li>
				<li id="homeLink"><a href="../" %(linkfade_home)s>Home</a></li>
			</ul>
			<div id="infoLinkWrapper">
				<div id="homeLinkInfo">&nbsp;</div>
				<div id="guideLinkInfo">&nbsp;</div>
				<div id="blogLinkInfo">&nbsp;</div>
				<div id="aboutLinkInfo">&nbsp;</div>
				<div id="contactLinkInfo">&nbsp;</div>
				<div id="loginLinkInfo">&nbsp;</div>
				<div id="registerLinkInfo">&nbsp;</div>
			</div>
		</div>
		%(content_div)s
		""" % {
			"title_name":			title_name,
			"javascript":			javascript,
			"css":					css,
			"linkfade_register":	linkfade('register'),
			"linkfade_login":		linkfade('login'),
			"linkfade_contact":		linkfade('contact'),
			"linkfade_about":		linkfade('about'),
			"linkfade_blog":		linkfade('blog'),
			"linkfade_guide":		linkfade('guide'),
			"linkfade_home":		linkfade('home'),
			"jquery_path":			jquery_path,
			"jqueryui_path":		jqueryui_path,
			"css_path":				css_path,
			"js_lib":				js_lib_s,
			
			"content_div":			content_div,
		}


def footers(with_analytics=True):
	if with_analytics:
		analytics = data['analytics']
	else:
		analytics = ""
	
	return """</div><!-- content -->
			<div class="clear">
				&nbsp;
			</div>
			</div><!-- page -->
			
			<div class="footer">
			<br />
			Game copyright <a href="http://woarl.com/blog">Teifion Jordan</a>, all rights reserved.<br />
			If you want to use these game rules for your own game, please contact Teifion, all player written stories and cultures are property of their authors
			</div><!-- footer -->
			%s
		</body>
	</html>""" % analytics


import html.entities
codepoint2name = html.entities.codepoint2name
def de_unicode(text):
	# text = "".join(("&%s;" % codepoint2name[ord(c)] if ord(c) in codepoint2name else c) for c in text)
	# text = text.replace("&lt;", '<').replace("&gt;", '>').replace("&quot;", "'").replace("&amp;nbsp;", "&nbsp;")
	# return text
	# text = text.replace("’", "'")
	
	# text = text.replace("", "")# Some random invisible character that Sharyk managed to put in an order once
	
	# text = text.replace("á", "&aacute;")
	# text = text.replace("í", "&iacute;")
	# text = text.replace("ó", "&oacute;")
	# text = text.replace("õ", "&otilde;")
	# text = text.replace("â", "&acirc;")
	# text = text.replace("ë", "&euml;")
	# text = text.replace("ç", "&ccedil;")
	# text = text.replace("è", "&egrave;")
	# text = text.replace("ü", "&uuml;")
	# 
	# text = text.replace("ō", "&otilde;")
	# text = text.replace("ś", "s")
	# text = text.replace("į", "i")
	# text = text.replace("ì", "&igrave;")
	# text = text.replace("å", "&aring;")
	# text = text.replace("ò", "&ograve;")
	# text = text.replace("õ", "&otilde;")
	# # text = text.replace("Î", "&Icirc;")
	# text = text.replace("Î", "I")
	
	text = text.replace("’", "&rsquo;")
	text = text.replace("‘", "&lsquo;")
	text = text.replace("“", "&ldquo;")
	text = text.replace("”", "&rdquo;")
	
	return text

