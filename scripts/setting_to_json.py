from obj_parser import parse_obj

data = open("setting.dat", "rb")

parsed = parse_obj(data)

import pprint as pprintlib
pprint = pprintlib.PrettyPrinter(sort_dicts=False).pprint

pprint(parsed)
