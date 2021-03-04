from obj_parser import parse_obj

data = open("setting.dat", "rb").read()

parsed, _ = parse_obj(data)

import pprint as pprintlib
pprint = pprintlib.PrettyPrinter(sort_dicts=False).pprint

pprint(parsed)
