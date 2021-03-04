import sys, os
from obj_ids import ID

srcdir = os.path.dirname(sys.argv[0])
compati_root = os.path.join(srcdir, "../decompiled/scripts/gudetama/data/compati/")

def do_create(longname):
	shortname = "obj" # ("".join([c for c in longname if c.isupper()])).lower()
	fname = os.path.join(compati_root, f"{longname}.as")
	write_src = open(fname).read().split("public function write(param1:ByteArray) : void")[1].split("{\n")[1].split("\n      }")[0]

	print(f"\n\telif obj_id == ID.{longname}:")
	print("\t\t" + shortname, "= {}")

	for line in write_src.split("\n"):
		line = line.strip()[:-1]
		if not line: continue
		if line.startswith("CompatibleDataIO"):
			fieldname = line.split(",")[1].strip(")").split("#")[0]
			if ",7)" in line:
				print(f"\t\t{shortname}[\"{fieldname}\"], data = parse_primitive_obj(ID(7), data)")
			elif ",8)" in line:
				print(f"\t\t{shortname}[\"{fieldname}\"], data = parse_primitive_obj(ID(8), data)")
			elif ",9)" in line:
				print(f"\t\t{shortname}[\"{fieldname}\"], data = parse_primitive_obj(ID(9), data)")
			else:
				print(f"\t\t{shortname}[\"{fieldname}\"], data = parse_obj(data)")
		elif "writeInt" in line:
			fieldname = line.split("(")[1].split(")")[0].split("#")[0]
			print(f"\t\t{shortname}[\"{fieldname}\"], data = unpackex(\"i\", data)")
		elif "writeShort" in line:
			fieldname = line.split("(")[1].split(")")[0].split("#")[0]
			print(f"\t\t{shortname}[\"{fieldname}\"], data = unpackex(\"h\", data)")
		elif "writeDouble" in line:
			fieldname = line.split("(")[1].split(")")[0].split("#")[0]
			print(f"\t\t{shortname}[\"{fieldname}\"], data = unpackex(\"d\", data)")
		elif "writeFloat" in line:
			fieldname = line.split("(")[1].split(")")[0].split("#")[0]
			print(f"\t\t{shortname}[\"{fieldname}\"], data = unpackex(\"f\", data)")
		elif "writeBoolean" in line or "writeByte" in line:
			fieldname = line.split("(")[1].split(")")[0].split("#")[0]
			print(f"\t\t{shortname}[\"{fieldname}\"], data = unpackex(\"b\", data)")
		elif "writeUTF" in line:
			fieldname = line.split("(")[1].split(")")[0].split("#")[0]
			print(f"\t\t{shortname}[\"{fieldname}\"], data = parseUTF(data)")
		else:
			exit("ERROR:" + line)

	#print(f"\t\treturn {shortname}, data")
	print(f"\t\treturn (\"{longname}\", {shortname}), data")

print("""\
# This file is AUTO GENERATED by parser_generator.py - DO NOT EDIT!
from obj_ids import ID
from parser_utils import *

def parse_compound_obj(obj_id, data, parse_obj, parse_primitive_obj):

\tif False: # just to get the elif chain started...
\t\tpass\
""")

for f in sorted(os.listdir(compati_root)):
	longname = f[:-3].strip("_")
	
	# skip objects that don't have an ID
	try:
		ID[longname]
	except KeyError:
		continue
	
	do_create(longname)