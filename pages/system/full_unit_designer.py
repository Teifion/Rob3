from pages import common
from data import equipment, equipment_q, resource_f


output		= ['<a href="unit.php" id="compact_link" class="block_link" style="text-align:center;">Compact designer</a><br />']


#	JAVASCRIPT
#------------------------
javascript	= ["""
function switch_to_tab (my_tab)
{
	var current_tab = $('#current_tab').html();
	
	if (my_tab == current_tab) return;
	
	// Tabs
	$('#' + current_tab + '_tab').removeClass('selected_equ_tab');
	$('#' + my_tab + '_tab').addClass('selected_equ_tab');
	
	// Hide, show
	$('#' + current_tab + '_div').fadeOut(250, function (){$('#' + my_tab + '_div').fadeIn(250);});
	$('#current_tab').html(my_tab);
}

function switch_to_section (my_section)
{
	var current_selector = $('#current_selector').html();
	
	if (my_section == current_selector) return;
	
	// Tabs
	$('#' + current_selector + '_row').removeClass('selector_row_selected');
	$('#' + my_section + '_row').addClass('selector_row_selected');

	$('#current_selection').fadeOut(250, function ()
	{
		$('#current_selection').html($('#' + my_section).html());
		$('#current_selection').fadeIn(250);
	});
	
	$('#current_selector').html(my_section);
}
"""]

#	CSS
#------------------------
css			= """
#tabs
{
	border-bottom:	1px solid #A00;
	width:	892px;
	height:	33px;
}

.equ_tab, .selected_equ_tab
{
	border-bottom:		3px solid #EEE;
	padding:			5px 0 0;
	width:				148px;
	text-align:			center;
	text-decoration:	none;
	float:				left;
	height:				25px;
	background-color:	#FFF;
	cursor:				pointer;
	font-weight:		bold;
	color:				#000;
}
 
.equ_tab:hover
{
	border-color:		#A00;
	color:				#000;
}
 
.selected_equ_tab, .selected_equ_tab:hover
{
	background-color:	#7F0000;
	color:				#FFF;
	border-bottom:		3px solid #A00;
}




.selector_row, .selector_row_selected
{
	border:	1px dotted #CCC;
	padding:3px;
	margin:	2px;
	float:	left;
	width:	200px;
	cursor:	pointer;
}

.selector_row:hover
{
	border-color:		#000;
	background-color:	#EEE;
}

.selector_row_selected, .selector_row_selected:hover
{
	border-style:		solid;
	border-color:		#A00;
	background-color:	#CCC;
}

#selections
{
	width:		870px;
	height:		300px;
	padding:	10px;
	
	overflow:	scroll;
}

#current
{
	border: 1px solid #AAA;
	width:	444px;
	float:	left;
}

#current_selection_wrapper
{
	border: 	1px solid #AAA;
	width:		444px;
	min-height:	300px;
	float:		right;
}
"""

#	PREP FOR OUTPUT
#------------------------
def item_selector(the_equipmet):
	"""The menu item within the tab"""
	return """
	<div id="e%(id)s_row" class="selector_row" onclick="switch_to_section('e%(id)s');">
		%(name)s
	</div>
	""" % {
		"id":	the_equipmet.id,
		"name":	the_equipmet.name,
	}

# equipment_list		= equipment.get_equipment_list()
# equipment_dict_c	= equipment.get_equipment_dict_c()
equipment_list, equipment_dict_c = equipment_q.get_public_equipment()



combat_output	= []
ranged_output	= []
armour_output	= []
shields_output	= []
beasts_output	= []
mounts_output	= []
training_output	= []

item_holders	= []# Stores information on the items

for e in equipment_list:
	the_equipment = equipment_dict_c[e]
	cat = equipment.cat_list[the_equipment.category]
	
	if cat in ("Boat hull","Custom","Balloon","Siege engine","Seabourne mount"): continue
	
	# The descriptior
	item_holders.append("""
	<div id="e%(id)s" style="display:none;">
		<span class="stitle">%(name)s</span>
		Description: %(description)s
	</div>
	""" % {
		"id":			e,
		"name":			the_equipment.name,
		"description":	the_equipment.description,
	})
	
	if cat in ('Sword','Axe','Hammer','Flail','Polearm','Dagger'):
		combat_output.append(item_selector(the_equipment))
	
	elif cat in ('Bow','Crossbow','Thrown','Gunpowder'):
		ranged_output.append(item_selector(the_equipment))
	
	elif cat == 'Armour':
		armour_output.append(item_selector(the_equipment))
	
	elif cat == 'Shield':
		shields_output.append(item_selector(the_equipment))
	
	elif cat == 'Mount':
		mounts_output.append(item_selector(the_equipment))
	
	elif cat == 'Beast':
		beasts_output.append(item_selector(the_equipment))
	
	elif cat == 'Training':
		training_output.append(item_selector(the_equipment))
	


#	OUTPUT
#------------------------
output.append("""
<span id="current_tab" style="display:none;">combat</span>
<span id="current_selector" style="display:none;"></span>
<div id="container">
	<div id="tabs">
		<a class="equ_tab" id="combat_tab" href="#" onclick="switch_to_tab('combat');return false;" style="width:149px;">Combat</a>
		<a class="equ_tab" id="ranged_tab" href="#" onclick="switch_to_tab('ranged');return false;" style="width:149px;">Ranged</a>
		<a class="equ_tab" id="armour_tab" href="#" onclick="switch_to_tab('armour');return false;" style="width:149px;">Armour</a>
		<a class="equ_tab" id="shields_tab" href="#" onclick="switch_to_tab('shields');return false;" style="width:149px;">Shields</a>
		<a class="equ_tab" id="beasts_tab" href="#" onclick="switch_to_tab('beasts');return false;">Beasts</a>
		<a class="equ_tab" id="mounts_tab" href="#" onclick="switch_to_tab('mounts');return false;">Mounts</a>
	</div>
	<div id="selections">
		<div id="combat_div">
			%(combat_div)s
			<div style="clear:both;">&nbsp;</div>
		</div>
		<div id="ranged_div" style="display:none;">
			%(ranged_div)s
			<div style="clear:both;">&nbsp;</div>
		</div>
		<div id="armour_div" style="display:none;">
			%(armour_div)s
			<div style="clear:both;">&nbsp;</div>
		</div>
		<div id="shields_div" style="display:none;">
			%(shields_div)s
			<div style="clear:both;">&nbsp;</div>
		</div>
		<div id="beasts_div" style="display:none;">
			%(beasts_div)s
			<div style="clear:both;">&nbsp;</div>
		</div>
		<div id="mounts_div" style="display:none;">
			%(mounts_div)s
			<div style="clear:both;">&nbsp;</div>
		</div>
		
	</div>
	<div id="current">
		Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
	</div>
	<div id="current_selection_wrapper">
		<div id="current_selection">
			&nbsp;
		</div>
	</div>
	<div style="clear:both">&nbsp;</div>
</div>
%(holders)s

<script type="text/javascript" charset="utf-8">
	$('#combat_tab').addClass('selected_equ_tab');
</script>
<!--
<script type="text/javascript" charset="utf-8">
	setTimeout($('html, body').animate({scrollTop: 200}),0);
</script>
-->
""" % {
	"combat_div":	"".join(combat_output),
	"ranged_div":	"".join(ranged_output),
	"armour_div":	"".join(armour_output),
	"shields_div":	"".join(shields_output),
	"beasts_div":	"".join(beasts_output),
	"mounts_div":	"".join(mounts_output),
	
	"holders":		"".join(item_holders),
})
# $('html, body').animate({scrollTop: $('#compact_link').offset().top-($(window).height()/2)});


print common.headers("Unit designer", css, "".join(javascript), local_path=1)
print "".join(output)
print common.footers()