import database

# Runs all checks
from reports import players_reports
from reports import city_reports
# import military_check
# import ops_check
# from checks import cities_check
# import teams_check

def main(verbose=False):
	cursor = database.get_cursor()
	output = []
	
	output.append(players_reports.run(cursor, verbose))
	output.append(city_reports.run(cursor, verbose))
	
	if output != []:
		print(database.shell_text("\n".join(output)))
	else:
		print(database.shell_text("[g]All reports green[/g]\n"))

if __name__ == '__main__':
	main()