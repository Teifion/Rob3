import database

# Runs all checks
from checks import cities_check
from checks import military_check
from checks import ops_check
from checks import players_check
from checks import teams_check

def main(cursor=None, check_all=False, verbose=True):
	if not cursor:
		cursor = database.get_cursor()
	
	if verbose:
		print(database.shell_text("''Starting system checks''"))
	
	cities_check.run(cursor, check_all, verbose)
	military_check.run(cursor, check_all, verbose)
	players_check.run(cursor, check_all, verbose)
	ops_check.run(cursor, check_all, verbose)
	teams_check.run(cursor, check_all, verbose)
	
	if verbose:
		print(database.shell_text("''Checks complete''"))
	
if __name__ == '__main__':
	main()