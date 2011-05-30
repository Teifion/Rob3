import time
from classes import team
from pages import common
from rules import unit_rules, spell_rules, tech_rules, team_rules

def spelling_compression(text):
	return text.replace("\t", "")#.replace("\n", "")
	
	# Function calls
	text = text.replace("add_option", "a_o")
	
	# Construction
	text = text.replace("building_array", "b_arr")
	text = text.replace("building_menu", "b_mnu")
	text = text.replace("wall_menu", "w_mnu")
	# migration_text_
	
	return text

def javascript(load_java, run_java):
	return """
	function on_load_setup ()
	{
		%(load_java)s
		
		$('#target_team_2').html($('#target_team_1').html());
		$('#target_team_3').html($('#target_team_1').html());
		
		$('#expected_allies_1').html($('#target_team_1').html());
		$('#expected_allies_2').html($('#target_team_1').html());
		$('#expected_allies_3').html($('#target_team_1').html());
		
		$('#target_city_2').html($('#target_city_1').html());
		$('#target_city_3').html($('#target_city_1').html());
		$('#target_city_4').html($('#target_city_1').html());
		$('#target_city_5').html($('#target_city_1').html());
		
		$('#armies_2').html($('#armies_1').html());
		$('#armies_3').html($('#armies_1').html());
		$('#armies_4').html($('#armies_1').html());
		$('#armies_5').html($('#armies_1').html());
		$('#armies_6').html($('#armies_1').html());
		$('#armies_7').html($('#armies_1').html());
		
		/* build_orders(); */
		$('#loading_div').hide();
		switch_to('overview');
		//switch_to('units');
		//switch_to('plan');
		//switch_to('feedback');
	}
	
	function on_keyup_run ()
	{
		//build_orders();
	}
	
	function on_change_run ()
	{
		//build_orders();
	}
	
	function clean_text (input_text)
	{
		return input_text.replace("\\t", "").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\\\", "");
	}
	
	function build_orders ()
	{
		var rob_block = '';
		var war_name = $('#war_name').val();
		
		var target_team = $('#target_team_1 option:selected').val();
		var targets = '';
		if (target_team != '')
		{
			targets += target_team;
			
			var target_team = $('#target_team_2 option:selected').val();
			if (target_team != '')
			{
				targets += ', ' + target_team;
				var target_team = $('#target_team_3 option:selected').val();
				if (target_team != '')
				{
					targets += ', ' + target_team;
				}
			}
			
			rob_block += '[b]Targets:[/b] ' + targets + '\\n';
		}
		
		var target_city = $('#target_city_1 option:selected').val();
		var cities = '';
		if (target_city != '')
		{
			cities += target_city;
			var target_city = $('#target_city_2 option:selected').val();
			if (target_city != '')
			{
				cities += ', ' + target_city;
				var target_city = $('#target_city_3 option:selected').val();
				if (target_city != '')
				{
					cities += ', ' + target_city;
					var target_city = $('#target_city_4 option:selected').val();
					if (target_city != '')
					{
						cities += ', ' + target_city;
						var target_city = $('#target_city_5 option:selected').val();
						if (target_city != '')
						{
							cities += ', ' + target_city;
						}
					}
				}
			}
			
			rob_block += '[b]Cities:[/b] ' + cities + '\\n';
		}
		
		var depart_time = $('#depart_time option:selected').val();
		var depart_month = $('#depart_month option:selected').val();
		if (depart_month != '')
		{
			if (depart_month != '')
			{
				rob_block += '[b]Departure:[/b] ' + depart_time + ' ' + depart_month + '\\n';
			}
			else
			{
				rob_block += '[b]Departure:[/b] ' + depart_month + '\\n';
			}
		}
		
		var expected_ally = $('#expected_allies_1 option:selected').val();
		var allies = '';
		if (expected_ally != '')
		{
			allies += expected_ally;
			var expected_ally = $('#expected_allies_2 option:selected').val();
			if (expected_ally != '')
			{
				allies += ', ' + expected_ally;
				var expected_ally = $('#expected_allies_3 option:selected').val();
				if (expected_ally != '')
				{
					allies += ', ' + expected_ally;
				}
			}
			
			rob_block += '[b]Allies:[/b] ' + allies + '\\n';
		}
		
		
		var army = $('#armies_1 option:selected').val();
		var armies = '';
		if (army != '')
		{
			armies += army;
			
			var army = $('#armies_2 option:selected').val();
			if (army != '') {armies += ', ' + army;}
			
			var army = $('#armies_3 option:selected').val();
			if (army != '') {armies += ', ' + army;}
			
			var army = $('#armies_4 option:selected').val();
			if (army != '') {armies += ', ' + army;}
			
			var army = $('#armies_5 option:selected').val();
			if (army != '') {armies += ', ' + army;}
			
			var army = $('#armies_6 option:selected').val();
			if (army != '') {armies += ', ' + army;}
			
			var army = $('#armies_7 option:selected').val();
			if (army != '') {armies += ', ' + army;}
			
			rob_block += '[b]Forces:[/b] ' + armies + '\\n';
		}
		
		var orders = '';
		
		var objectives = $('#objectives').val();
		if (objectives != '')
		{
			orders += '[b]Objectives:[/b]\\n' + objectives + '\\n\\n';
		}
		
		var timeline = $('#timeline').val();
		if (timeline != '')
		{
			orders += '[b]Timeline:[/b]\\n' + timeline + '\\n\\n';
		}
		
		var plan = $('#plan').val();
		if (plan != '')
		{
			orders += '[b]Plan:[/b]\\n' + plan + '\\n\\n';
		}
		
		var reminders = $('#reminders').val();
		if (reminders != '')
		{
			orders += '[b]Reminders:[/b]\\n' + reminders + '\\n\\n';
		}
		
		var ofinally = $('#finally').val();
		if (ofinally != '')
		{
			orders += '[b]Finally:[/b]\\n' + ofinally + '\\n\\n';
		}
		
		var feedback = $('#feedback').val();
		if (feedback != '')
		{
			orders += '[b]Feedback:[/b]\\n' + feedback + '\\n\\n';
		}
		
		var final_output = '[o]' + war_name + '[/o]\\n[rob]' + rob_block + '[/rob]\\n\\n' + orders;
		final_output = clean_text(final_output);
		$('#final_output').text(final_output);
	}

	function hide_all_sections ()
	{
		$('#overview_div').hide();
		$('#units_div').hide();
		$('#plan_div').hide();
		$('#feedback_div').hide();
	
		$('#overview_tab').removeClass('ti_tab_selected');
		$('#units_tab').removeClass('ti_tab_selected');
		$('#plan_tab').removeClass('ti_tab_selected');
		$('#feedback_tab').removeClass('ti_tab_selected');
	}

	function switch_to (div_name)
	{
		hide_all_sections();
		$('#' + div_name + '_div').show();
		$('#' + div_name + '_tab').addClass('ti_tab_selected');
	}

	""" % {
		"load_java":	load_java,
		"run_java":		run_java,
	}