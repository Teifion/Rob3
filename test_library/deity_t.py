import math
import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library import orders_t_lib

from test_library.deity_sets import arl_t
from test_library.deity_sets import trchkithin_t
from test_library.deity_sets import adyl_t
from test_library.deity_sets import ssai_t
from test_library.deity_sets import orakt_t
from test_library.deity_sets import agashn_t
from test_library.deity_sets import ldura_t
from test_library.deity_sets import azmodius_t
from test_library.deity_sets import phraela_and_caist_t
from test_library.deity_sets import soag_chi_t
from test_library.deity_sets import khystrik_t
from test_library.deity_sets import laegus_t
from test_library.deity_sets import zasha_t
from test_library.deity_sets import alki_t

class Arl_favour_tester(arl_t.Arl_favour_tester): pass
class Trchkithin_favour_tester(trchkithin_t.Trchkithin_favour_tester): pass
class Adyl_favour_tester(adyl_t.Adyl_favour_tester): pass
class Ssai_favour_tester(ssai_t.Ssai_favour_tester): pass
class Orakt_favour_tester(orakt_t.Orakt_favour_tester): pass
class Agashn_favour_tester(agashn_t.Agashn_favour_tester): pass
class Ldura_favour_tester(ldura_t.Ldura_favour_tester): pass
class Azmodius_favour_tester(azmodius_t.Azmodius_favour_tester): pass
class Phraela_and_Caist_favour_tester(phraela_and_caist_t.Phraela_and_Caist_favour_tester): pass
class Soag_chi_favour_tester(soag_chi_t.Soag_chi_favour_tester): pass
class Khystrik_favour_tester(khystrik_t.Khystrik_favour_tester): pass
class Laegus_favour_tester(laegus_t.Laegus_favour_tester): pass
class Zasha_favour_tester(zasha_t.Zasha_favour_tester): pass
class Alki_favour_tester(alki_t.Alki_favour_tester): pass