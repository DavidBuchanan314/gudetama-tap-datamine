import struct


def unpackex(fmt, data):
	fmt = ">" + fmt
	size = struct.calcsize(fmt)
	res = struct.unpack(fmt, data.read(size))
	if len(res) == 1:
		return res[0]
	return res


def parseUTF(data):
	length = unpackex("H", data)
	return data.read(length).decode()


def parseByteArray(data):
	length = unpackex("H", data)
	return data.read(length)
