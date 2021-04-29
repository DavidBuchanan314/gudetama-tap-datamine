import sys
import json
import requests
from pathlib import Path

# https://stackoverflow.com/a/16696317/4454877
def download_file(url, local_filename):
	filepath = Path(local_filename)
	if filepath.is_file():
		return # TODO: check file hashes for updates?
	print(url)
	#exit()
	filepath.parents[0].mkdir(parents=True, exist_ok=True)
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192): 
				f.write(chunk)


data = json.load(open(sys.argv[1]))

cdn = data["resourceUrl"].replace("http://", "https://")  # always use protection!
cdn = "https://gudetama101.cyberstep.jp:8443/gde/static/"

for i, fileinfo in enumerate(data["fileInfos"]):
	filepath = fileinfo["path"]
	url = cdn + filepath
	localpath = "../assets/" + filepath
	#print(f"({i}/{len(data['fileInfos'])}) Saving {url} to {localpath}")
	try :
		download_file(url, localpath)
	except requests.exceptions.HTTPError:
		print("HTTP ERROR!!!!!")
		pass
