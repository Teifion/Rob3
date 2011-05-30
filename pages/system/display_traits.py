import pages.site.trait_p

# from pages.sites import trait_p
page_data = {
	"Header": True
}


def main(cursor):
	return pages.site.trait_p.trait_list(cursor)