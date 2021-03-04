import struct
from compound_obj_parser import parse_compound_obj
from obj_ids import ID
from parser_utils import *


def parse_primitive_obj(obj_id, data):
	if obj_id == ID.NULL:
		return None, data

	if obj_id == ID.OBJECT_ARRAY:
		num_objs, data = unpackex("H", data)
		#print(num_objs)
		#print("num_objs:", num_objs)
		result = []
		for _ in range(num_objs):
			res, data = parse_obj(data)
			#print(res)
			result.append(res)
		return result, data

	elif obj_id == ID.INT_ARRAY:
		num_ints, data = unpackex("H", data)
		#print("num_ints:", num_ints)
		result = []
		for _ in range(num_ints):
			res, data = unpackex("i", data)
			result.append(res)
		return result, data

	elif obj_id == ID.SHORT_ARRAY:
		num_ints, data = unpackex("H", data)
		#print("num_ints:", num_ints)
		result = []
		for _ in range(num_ints):
			res, data = unpackex("h", data)
			result.append(res)
		return result, data


	elif obj_id == ID.ByteArray:
		#print(data)
		bytes_len, data = unpackex("I", data)
		the_bytes, data = data[:bytes_len], data[bytes_len:]
		#print(the_bytes)
		return the_bytes, data

	elif obj_id == ID.FLOAT_ARRAY:
		num_ints, data = unpackex("H", data)
		#print("num_ints:", num_ints)
		result = []
		for _ in range(num_ints):
			res, data = unpackex("f", data)
			result.append(res)
		return result, data


	elif obj_id == ID.String:
		str_len, data = unpackex("H", data)
		the_str, data = data[:str_len], data[str_len:]
		#print(the_str)
		return the_str.decode(), data

	elif obj_id == ID.INTHASHMAP:
		num_entries, data = unpackex("H", data)
		ihm = {}
		for _ in range(num_entries):
			intkey, data = unpackex("I", data)
			value, data = parse_obj(data)
			#print(intkey, value)
			ihm[intkey] = value
		return ihm, data

	elif obj_id == ID.HASHMAP:
		#print(data[:200])
		num_entries, data = unpackex("H", data)
		#print(num_entries)
		hm = {}
		for _ in range(num_entries):
			key, data = parseUTF(data)
			#print(key)
			value, data = parse_obj(data)
			#print(value)
			hm[key] = value
		return hm, data

	elif obj_id == ID.ARRAYLIST: # XXX same as object array?
		num_objs, data = unpackex("H", data)
		#print(num_objs)
		#print("num_objs:", num_objs)
		result = []
		for _ in range(num_objs):
			res, data = parse_obj(data)
			#print(res)
			result.append(res)
		return result, data

	elif obj_id == ID.INT:
		return unpackex("i", data)

	elif obj_id == ID.SHORT:
		return unpackex("h", data)

def parse_obj(data):
	obj_id_int, data = unpackex("H", data)
	obj_id = ID(obj_id_int)

	if obj_id_int < 12:
		return parse_primitive_obj(obj_id, data)
	else:
		return parse_compound_obj(obj_id, data, parse_obj, parse_primitive_obj)
