import sys
import re
from pages import common
from pages import site
from lore import pages
import string
from queries import deity_q

def minify(source):
	"""docstring for minify"""
	source = source.replace('\n', ' ')
	source = source.replace('	', ' ')
	source = source.replace('  ', ' ')
	source = source.replace('  ', ' ')
	source = source.replace('  ', ' ')
	# source = re.sub(r'<!--[^-->]-->', "", source) # Not convinced about this working flawlessly
	return source

def minify_css(css):
	"""docstring for minifyCSS"""
	# return css# Comment out this line to make it minify
	output = ''
	
	# remove comments - this will break a lot of hacks :-P
	css = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", css )
	css = re.sub( r'/\*[\s\S]*?\*/', "", css )
	css = css.replace( "$$HACK1$$", '/**/' ) # preserve IE<6 comment hack
	
	# url() don't need quotes
	css = re.sub( r'url\((["\'])([^)]*)\1\)', "url(\\2)", css )
	
	# spaces may be safely collapsed as generated content will collapse them anyway
	css = re.sub( r'\s+', " ", css )
	
	for rule in re.findall( r'([^{]+){([^}]*)}', css ):
		selectors = []
		for selector in rule[0].split( ',' ):
			selectors.append( selector.strip() )
			
		# order is important, but we still want to discard repetitions
		properties = {}
		porder	= []
		for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
			key = prop[0].strip().lower()
			if key not in porder:
				porder.insert( 0, key )
			properties[ key ] = prop[1].strip()
		porder.reverse()
		
		# output rule if it contains any declarations
		if len(properties) > 0:
			s = '';
			for key in porder:
				s += key + ":" + properties[key] + ";"
			output += ",".join( selectors ) + "{" + s + "}"
	
	return output

nav_bar = """
<div class="navigation">
	<ul>
		<li class="navHeading">General pages</li>
		<li><a href="index.html">Homepage</a></li>
		<li><a href="http://woarl.com/board/index.php">Web Board</a></li>
		<li><a href="pages/general/gateway.html">The Gateway</a></li>
		<li><a href="pages/general/history.html">The Backstory</a></li>
		<li><a href="pages/general/contact.html">Contact me</a></li>
	</ul>
	<div class="navDrop">
		&nbsp;
	</div>
	<ul>
		<li class="navHeading">How to play</li>
		<li><a href="pages/general/starting.html">How to start playing</a></li>
		<li><a href="pages/general/orders.html">How to write orders</a></li>
		<li><a href="pages/general/improvement.html">How to improve the game</a></li>
		<li><a href="pages/nations/cultures.html">Nations and Cultures</a></li>
		<li><a href="pages/rob/index.html">Rob the Database</a></li>
		<li><a href="pages/general/crazy.html">Crazy projects</a></li>
	</ul>
	<div class="navDrop">
		&nbsp;
	</div>
	<ul>
		<li class="navHeading">Nations</li>
		<li><a href="pages/nations/chosen.html">The Chosen Ones</a></li>
		<li><a href="pages/nations/evolution.html">Evolution</a></li>
		<li><a href="pages/nations/evoList.html">List of Evolutions</a></li>
		<li><a href="pages/nations/economy.html">Economy</a></li>
		<li><a href="pages/nations/technology.html">Technology</a></li>
		<li><a href="pages/nations/construction.html">Construction</a></li>
		<li><a href="pages/nations/building_list.html">Building list</a></li>
		<li><a href="pages/nations/ir.html">Indigenous Races</a></li>
	</ul>
	<div class="navDrop">
		&nbsp;
	</div>
	<ul>
		<li class="navHeading">Military rules</li>
		<li><a href="pages/military/army.html">The army</a></li>
		<li><a href="pages/military/navy.html">The navy</a></li>
		<li><a href="pages/military/naval_guide.html">Naval guide</a></li>
		<li><a href="pages/military/unit.html">Unit designer</a></li>
		<li><a href="pages/military/spies.html">Covert operatives</a></li>
		<li><a href="pages/military/beasts.html">The beasts of the wild</a></li>
		<li><a href="pages/military/list_mounts.html">Mount list</a></li>
		<li><a href="pages/military/list_beasts.html">Beast list</a></li>
	</ul>
	<div class="navDrop">
		&nbsp;
	</div>
	<ul>
		<li class="navHeading">Magical rules</li>
		<li><a href="pages/magic/how.html">How magic works</a></li>
		<li><a href="pages/magic/spells.html">Spell list</a></li>
		<li><a href="pages/magic/light.html">Light spells</a></li>
		<li><a href="pages/magic/dark.html">Dark spells</a></li>
		<li><a href="pages/magic/destruction.html">Destruction spells</a></li>
		<li><a href="pages/magic/abjuration.html">Abjuration spells</a></li>
		<li><a href="pages/magic/daemonic.html">Daemonic spells</a></li>
		<li><a href="pages/magic/necromancy.html">Necromancy spells</a></li>
		<li><a href="pages/magic/alchemy.html">Alchemy combinations</a></li>
		<li><a href="pages/magic/enchantment.html">Enchantment effects</a></li>
		<li><a href="pages/magic/worlds.html">World list</a></li>
		<li><a href="pages/magic/progression.html">Daemonic progression</a></li>
	</ul>
	<div class="navDrop">
		&nbsp;
	</div>
	<ul>
		<li class="navHeading">Deity rules</li>
		<li><a href="pages/deity/gods.html">How deities function</a></li>
		<li><a href="pages/deity/pantheon.html">The pantheon</a></li>
	</ul>
	
	<!--
	<div class="navDrop">
		&nbsp;
	</div>
	<ul>
		<li class="navHeading">Other games</li>
		<li><a href="http://shatter.woarl.com/">Darkscapes</a></li>
	</ul>
	-->
	
	<div class="navDrop">
		&nbsp;
	</div>
	<br />
</div><!-- end of navigation -->
"""

# if (file_exists('includes/navigation.php'))
# {
# 	echo $links;
# }
# elseif (file_exists('../includes/navigation.php'))
# {
# 	$links = str_replace('href="pages/', 'href="../pages/', $links);
# 	$links = str_replace('href="index.php', 'href="../index.php', $links);
# 	
# 	echo $links;
# }
# else
# {
# 	$links = str_replace('href="pages/', 'href="../', $links);
# 	$links = str_replace('href="index.php', 'href="../../index.php', $links);
# 	
# 	echo $links;
# }

def _wrap_template(source, title):
	output = []
	
	output.append(common.headers(title, css="", javascript="", local_path=False, js_libs=[], tiers=2, content_div=False))
	output.append(nav_bar)
	output.append("<div class='content'>")
	output.append(source)
	output.append("</div>")
	output.append(common.footers(with_analytics=True))
	
	return "".join(output)

page_list = (
	#	Main site
	#------------------------
	("site", "index", site.standard_page, {}, "World of Arl"),
	
	#	General
	#------------------------
	("general", "starting", site.standard_page, {}, "How to start playing"),
	("general", "orders", site.standard_page, {}, "How to write orders"),
	
	#	Deities
	#------------------------
	# pages.append('pages/deity/gods')
	# pages.append('pages/deity/pantheon')
	("deities", "adyl", site.deity_info, {}, "Adyl"),
	("deities", "agashn", site.deity_info, {}, "Agashn"),
	("deities", "alki", site.deity_info, {}, "Alki"),
	("deities", "arl", site.deity_info, {}, "Arl"),
	("deities", "azmodius", site.deity_info, {}, "Azmodius"),
	("deities", "khystrik", site.deity_info, {}, "Khystrik"),
	("deities", "laegus", site.deity_info, {}, "Laegus"),
	("deities", "ldura", site.deity_info, {}, "Ldura"),
	("deities", "orakt", site.deity_info, {}, "Orakt"),
	("deities", "phraela_and_caist", site.deity_info, {"name":"Phraela and Caist"}, "Phraela and Caist"),
	("deities", "soag_chi", site.deity_info, {"name":"Soag chi"}, "Soag chi"),
	("deities", "ssai", site.deity_info, {}, "Ssai"),
	("deities", "trchkithin", site.deity_info, {}, "Trchkithin"),
	("deities", "zasha", site.deity_info, {}, "Zasha"),
	
	# Irs
	# ("irs", "jaegis", deity_info, {}),
	
	# Spells
	# ("spells", "creation", deity_info, {}),
	
	#	Nations
	#------------------------
	("nations", "chosen", site.standard_page, {}, "Chosen ones"),
	("nations", "construction", site.standard_page, {}, "Construction"),
	("nations", "building_list", site.building_list, {}, "Building list"),
	("nations", "cultures", site.standard_page, {}, "Cultures"),
	("nations", "economy", site.standard_page, {}, "Economics"),
	("nations", "evolution", site.standard_page, {}, "Evolution"),
	("nations", "evolution_list", site.evolution_list, {}, "Evolution list"),
	("nations", "happiness", site.standard_page, {}, "Happiness"),
	("nations", "ir", site.standard_page, {}, "Indiginous races"),
	("nations", "technology", site.standard_page, {}, "Technology"),
	("nations", "trait_list", site.trait_list, {}, "Traits list"),
	
	#	Monsters
	#------------------------
	("monsters", "costal_salamander", site.monster_info, {"name":"Costal salamander"}, "Costal salamander"),
	("monsters", "tishrashi_condor", site.monster_info, {"name":"Tishrashi condor"}, "Tishrashi condor"),
	("monsters", "gorquithor", site.monster_info, {}, "Gorquithor"),
	("monsters", "gryphon", site.monster_info, {}, "Gryphon"),
	("monsters", "hydra", site.monster_info, {}, "Hydra"),
	("monsters", "karithor", site.monster_info, {}, "Karithor"),
	("monsters", "murdaphant", site.monster_info, {}, "Murdaphant"),
	# ("monsters", "peyam", site.monster_info, {}, "Peyam"),
	("monsters", "troll", site.monster_info, {}, "Troll"),
	# ("monsters", "unicorn", site.monster_info, {}, "Unicorn"),

	#	General
	#------------------------
	("general", "about", site.standard_page, {}, "About us"),
	("general", "contact", site.standard_page, {}, "Contact us"),
	("general", "crazy", site.standard_page, {}, "Crazy projects"),
	("general", "gateway", site.standard_page, {}, "Gateway"),
	("general", "history", site.standard_page, {}, "The backstory"),
	("general", "improvement", site.standard_page, {}, "Improvement"),
	("general", "orders", site.standard_page, {}, "Orders"),
	
	#	Guide
	#------------------------
	("guide", "index", site.standard_page, {}, "The guide"),
	
	#	Magic
	#------------------------
	("magic", "how", site.standard_page, {}, "How magic works"),
	("magic", "progression", site.standard_page, {}, "Daemonic progression"),
	("magic", "spells", site.standard_page, {}, "Spell overview"),
	("magic", "worlds", site.standard_page, {}, "Worlds"),
	("magic", "light", site.spell_list, {}, "Light magic"),
	("magic", "dark", site.spell_list, {}, "Dark magic"),
	("magic", "destruction", site.spell_list, {}, "Destruction magic"),
	("magic", "abjuration", site.spell_list, {}, "Abjuration magic"),
	("magic", "daemonic", site.spell_list, {}, "Daemonic magic"),
	("magic", "necromancy", site.spell_list, {}, "Necromantic magic"),
	("magic", "alchemy", site.spell_list, {}, "Alchemical magic"),
	("magic", "enchantment", site.spell_list, {}, "Enchantement magic"),
	("magic", "animation", site.spell_list, {}, "Animation magic"),
	("magic", "sourcery", site.spell_list, {}, "Sourcery"),
	
	#	Military
	#------------------------
	("military", "army", site.standard_page, {}, "Armies"),
	("military", "equipment", site.standard_page, {}, "Equipment list"),
	("military", "navy", site.standard_page, {}, "Navies"),
	("military", "naval_guide", site.standard_page, {}, "Naval warfare"),
	("military", "spies", site.standard_page, {}, "Spies and operatives"),
	("military", "unit", site.standard_page, {}, "Unit designer"),
	
	#	Rob
	#------------------------
	# pages.append('pages/rob/index')
	# pages.append('pages/rob/orders')
	# pages.append('pages/rob/commands')
)

def make_page(cursor, cat, page, write_func, wrap_title, kwargs, verbose):
	source = write_func(cursor, cat, page, **kwargs)
	if wrap_title != "":
		source = _wrap_template(source, wrap_title)
	
	# source = pages.get_html(cursor, cat, page, level="public")
	path = '%s/pages/%s/%s.html' % (common.data['rob_site'], cat, page)
	if cat == "site" and page == "index":
		path = '%s/%s.html' % (common.data['rob_site'], page)
		source = source.replace("../../", "")
	else:
		source = source.replace('href="pages/', 'href="../')
		source = source.replace('href="index.html', 'href="../../index.html')
	
	try:
		f = open(path, 'w')
		
		# f.write(common.headers(title, css="", javascript="", local_path=False, js_libs=[], tiers=2).replace(
		# 	'<div class="contentWide" style="padding: 0px; width: 892px;">', ''
		# ))
		# f.write(nav_bar)
		# f.write("<div class='content'>")
		# f.write(source)
		# f.write("</div>")
		# f.write(common.footers(with_analytics=True))
		
		f.write(source)
		
		f.close()
	except IOError as e:
		print("File path %s could not be saved to" % path)
		raise
	except Exception as e:
		raise
	
	if verbose:
		print("%s/%s.html" % (cat, page))
	

# 	pageSource = pageSource.replace('.php', '.html')
# 	
# 	# Forum links need to stay as .php ;)
# 	pageSource = pageSource.replace('ucp.html', 'ucp.php')
# 	pageSource = pageSource.replace('feed.html', 'feed.php')
# 	pageSource = pageSource.replace('board/index.html', 'board/index.php')
# 	pageSource = pageSource.replace('board/viewforum.html', 'board/viewforum.php')
# 	pageSource = pageSource.replace('board/viewtopic.html', 'board/viewtopic.php')
# 	
# 	ext = 'html'
# 	if page == '404':
# 		pass
# 		# ext = 'shtml'
# 	
# 	f = open(('output/%s.%s' % (page, ext)), 'w')
# 	f.write(pageSource)

direct_copy = (
	# CSS
	# ('%s/styles.css' % (common.data['woa_folder']), '%s/styles.css' % (common.data['rob_site'])),
	
	# Jquery
	('%s/includes/jquery.js' % (common.data['woa_folder']), '%s/includes/jquery.js' % (common.data['rob_site'])),
	('%s/includes/jquery-ui.js' % (common.data['woa_folder']), '%s/includes/jquery-ui.js' % (common.data['rob_site'])),
)

direct_bin_copy = (
	# Layout images
	('%s/images/layout/bodyBG.jpg' % (common.data['woa_folder']), '%s/images/layout/bodyBG.jpg' % (common.data['rob_site'])),
	('%s/images/layout/headerBG.jpg' % (common.data['woa_folder']), '%s/images/layout/headerBG.jpg' % (common.data['rob_site'])),
	('%s/images/layout/footerBG.png' % (common.data['woa_folder']), '%s/images/layout/footerBG.png' % (common.data['rob_site'])),
	
	# Buttons
	('%s/images/buttons/headerNav.png' % (common.data['woa_folder']), '%s/images/buttons/headerNav.png' % (common.data['rob_site'])),
)

def build(cursor, verbose=True):
	# Libs
	for c, p in direct_copy:
		try:
			with open(c) as f:
				content = f.read()
			with open(p, 'w') as f:
				f.write(content)
		except Exception as e:
			print("Error copying %s to %s" % (c, p))
			raise
	
	# Images
	for c, p in direct_bin_copy:
		try:
			with open(c, mode='rb') as f:
				content = f.read()
			with open(p, mode='wb') as f:
				f.write(content)
		except Exception as e:
			print("Error copying %s to %s" % (c, p))
			raise
	
	# Pages
	for cat, page, write_func, kwargs, wrap_title in page_list:
		try:
			make_page(cursor, cat, page, write_func, wrap_title, kwargs, verbose)
		except Exception as e:
			print("Error on %s.%s" % (cat, page))
			raise
	
