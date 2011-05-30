import database
from data_classes import lore_entry

def new_entry(cat, page):
	return ["INSERT INTO lore_entries (cat, page) values ('%s', '%s');" % (database.escape(cat.lower().replace(" ", "_")), database.escape(page.lower().replace(" ", "_")))]

def new_block(entry_id, block):
	return ["INSERT INTO lore_blocks (entry, description, title, level, no_break, name) values (%d, '%s', '%s', %d, %s, '%s');" % (
		entry_id,
		database.escape(block['text']),
		database.escape(block.get('title', '')),
		lore_entry.levels.index(block.get('level', 'public')),
		block.get('no_break', False),
		database.escape(block.get('id', '')),
	)]
