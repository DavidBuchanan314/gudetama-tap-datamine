import struct


def unpackex(fmt, data):
	fmt = ">" + fmt
	size = struct.calcsize(fmt)
	return struct.unpack(fmt, data[:size]) + (data[size:],)


def packex(fmt, *data):
	return struct.pack(">" + fmt, *data)


def parseUTF(data):
	length, data = unpackex("H", data)
	string, data = data[:length], data[length:]
	return string.decode(), data


def parseByteArray(data):
	length, data = unpackex("H", data)
	string, data = data[:length], data[length:]
	return string, data
