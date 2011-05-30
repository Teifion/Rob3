from pages import common
from data import feat_f

player_id	= int(common.get_val("player", 0))
feat_id		= int(common.get_val("feat", 0))
feat_level	= int(common.get_val("feat_level", 0))

feat_f.set_feat(player_id, feat_id, feat_level)

print "location: edit_player&amp;player=%d" % player_id