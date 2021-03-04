from obj_parser import parse_obj
import json
import base64
import sys
import zlib
import io


# This lets us convert bytes to json, as a base64 string
class Base64Encoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, bytes):
			return base64.b64encode(o).decode()
		return json.JSONEncoder.default(self, o)


def setting_to_json(inpath, outpath):
	with open(inpath, "rb") as datafile:
		decompressed = zlib.decompress(datafile.read())
		parsed = parse_obj(io.BytesIO(decompressed))

	with open(outpath, 'w') as outfile:
		json.dump(parsed, outfile, cls=Base64Encoder, indent=2)


if __name__ == "__main__":
	setting_to_json(sys.argv[1], sys.argv[1]+".json")
