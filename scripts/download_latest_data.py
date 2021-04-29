import requests
import io
import sys
import os
import os.path
from obj_parser import parse_obj
from setting_to_json import setting_to_json

LOCALES = [
	"ja",
	"en",
	"ko",
	"cn",
	"tw"
]

CDN_BASE = "https://gudetama101.cyberstep.jp:8443/gde/static/setting/"
srcdir = os.path.dirname(sys.argv[0])
datdir = os.path.join(srcdir, "../datfiles/")
jsondir = os.path.join(srcdir, "../jsonfiles/")

s = requests.session()

# get game settings version
r = s.get("https://gudetama102.cyberstep.jp:8443/gde/direct?d=g")
version, unk = parse_obj(io.BytesIO(r.content[1:]))

print("VERSION:", version)

for locale in LOCALES:
	if locale == "ja":
		localestr = ""
	else:
		localestr = locale + "."
	filename = f"setting.dat.{localestr}{version}.34"
	url = CDN_BASE + filename
	destpath = os.path.join(datdir, filename)
	jsonpath = os.path.join(jsondir, filename + ".json")
	
	print("Getting", url)
	
	if os.path.isfile(destpath):
		print(destpath, "already exists, skipping.")
		continue
	
	r = s.get(url)
	assert(r.ok)
	
	print("Saving to", destpath)
	with open(destpath, "wb") as outfile:
		outfile.write(r.content)
	
	print("Converting to json...")
	setting_to_json(destpath, jsonpath)
