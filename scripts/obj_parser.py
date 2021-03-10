import struct
from compound_obj_parser import parse_compound_obj
from obj_ids import ID
from parser_utils import *


def parse_primitive_obj(obj_id, data):
	if obj_id == ID.NULL:
		return None

	if obj_id == ID.OBJECT_ARRAY:
		num_objs = unpackex("H", data)
		result = []
		for _ in range(num_objs):
			res = parse_obj(data)
			result.append(res)
		return result

	elif obj_id == ID.INT_ARRAY:
		num_ints = unpackex("H", data)
		result = []
		for _ in range(num_ints):
			res = unpackex("i", data)
			result.append(res)
		return result

	elif obj_id == ID.SHORT_ARRAY:
		num_ints = unpackex("H", data)
		result = []
		for _ in range(num_ints):
			res = unpackex("h", data)
			result.append(res)
		return result

	elif obj_id == ID.ByteArray:
		bytes_len = unpackex("I", data)
		return data.read(bytes_len)

	elif obj_id == ID.FLOAT_ARRAY:
		num_ints = unpackex("H", data)
		result = []
		for _ in range(num_ints):
			res = unpackex("f", data)
			result.append(res)
		return result

	elif obj_id == ID.String:
		str_len = unpackex("H", data)
		return data.read(str_len).decode()

	elif obj_id == ID.INTHASHMAP:
		num_entries = unpackex("H", data)
		ihm = {}
		for _ in range(num_entries):
			intkey = unpackex("I", data)
			value = parse_obj(data)
			ihm[intkey] = value
		return ihm

	elif obj_id == ID.HASHMAP:
		num_entries = unpackex("H", data)
		hm = {}
		for _ in range(num_entries):
			key = parseUTF(data)
			value = parse_obj(data)
			hm[key] = value
		return hm

	elif obj_id == ID.ARRAYLIST: # XXX same as object array?
		num_objs = unpackex("H", data)
		result = []
		for _ in range(num_objs):
			res = parse_obj(data)
			result.append(res)
		return result

	elif obj_id == ID.INT:
		return unpackex("i", data)

	elif obj_id == ID.SHORT:
		return unpackex("h", data)
	
	else:
		exit("bad id")

def parse_obj(data, compact=True):
	# TODO: if data is bytes, convert to BytesIO
	obj_id_int = unpackex("H", data)
	obj_id = ID(obj_id_int)

	if obj_id_int < 12:
		return parse_primitive_obj(obj_id, data)
	else:
		# we have to pass in the other parsers here, to avoid circular imports
		obj = parse_compound_obj(obj_id, data, parse_obj, parse_primitive_obj)
		return obj[1] if compact else obj
