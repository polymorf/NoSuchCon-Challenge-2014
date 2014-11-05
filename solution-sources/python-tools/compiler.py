
from pickletools import dis

def op_global(params):
	ret = "c"
	mod, func = params.strip("'").split(" ")
	ret += mod + "\n"
	ret += func + "\n"
	return ret

def op_reduce(params):
	return "R"

def op_mark(params):
	return "("

def op_string(params):
	ret = "S"
	ret += params
	ret += "\n"
	return ret

def op_int(params):
	ret = "I"
	ret += params
	ret += "\n"
	return ret

def op_tuple(params):
	return "t"

def op_list(params):
	return "l"

def op_dict(params):
	return "d"

def op_stop(params):
	return '.'

def op_setitem(params):
	return 's'

def op_put(params):
	return 'p' + params + '\n'

def op_get(params):
	return 'g' + params + '\n'

def op_build(params):
	return 'b'

def op_append(params):
	return 'a'

opcodes = {
	'GLOBAL': op_global,
	'REDUCE': op_reduce,
	'MARK': op_mark,
	'STRING': op_string,
	'INT': op_int,
	'TUPLE': op_tuple,
	'DICT': op_dict,
	'LIST': op_list,
	'STOP': op_stop,
	'SETITEM': op_setitem,
	'PUT': op_put,
	'GET': op_get,
	'BUILD': op_build,
	'APPEND': op_append,
}

def compiler():
	ret = ""
	with open('pickle.as') as f:
		for l in f:
			if l[0] == ';':
				continue
			l = l.replace("\n","").strip()
			if " " in l:
				op, params = l.split(" ", 1)
			else:
				op = l
				params = None
			if op == '':
				continue
			ret += opcodes[op](params)
	return ret
