import ctypes
import re


c_api: ctypes.CDLL | None = None  # will be initialized in init() in "frams.py". This variable is global because all ExtValue objects use it extensively.


class ExtValue[T]:  # Note: Python 3.12+ syntax allows for type variable T
	"""All Framsticks objects and values are instances of this class. Read the documentation of the 'frams' module for more information."""

	_reInsideParens = re.compile(r'\((.*)\)')
	_reservedWords = ['import']  # this list is scanned during every attribute access; only add what is really clashing with Framsticks properties
	_reservedXWords = ['x' + word for word in _reservedWords]
	_encoding = 'utf-8'


	def __init__(self, arg=None, dontinit=False):
		if dontinit:
			return

		if isinstance(arg, int):
			self._initFromInt(arg)
		elif isinstance(arg, str):
			self._initFromString(arg)
		elif isinstance(arg, float):
			self._initFromDouble(arg)
		elif arg is None:
			self._initFromNull()
		else:
			raise ctypes.ArgumentError("Can't make ExtValue from '%s' (%s)" % (str(arg), type(arg)))

		# Bypass our custom __setattr__ (just like a regular self.myfield=... assignment here, it would cause infinite recursion because our custom __setattr__ creates another ExtValue object) by calling object.__setattr__ directly:
		# object.__setattr__(self, 'debuginfo', "typ=%s, class=%s, arg=%s" % (str(self._type()), str(self._class()), str(arg)))  # for debugging the order of deletion/destruction of ExtValue objects


	def __del__(self):
		# debuginfo = self.__dict__['debuginfo'] if 'debuginfo' in self.__dict__ else '(not-inited)'
		if c_api is not None:  # There is some unknown interaction between the native Framsticks library and other native Python libraries (like numpy) that affects the order of the Python interpreter's garbage collection. This leads to occasional calls to this destructor after c_api becomes None (when the Python interpreter exits). Hence, this protection is included to avoid calling extFree() on None. An alternative would be to use self._finalizer = weakref.finalize(self, c_api.extFree, self.__ptr) instead of __del__.
			#print("\tDeleter of the object with debuginfo='%s'" % debuginfo)
			c_api.extFree(self.__ptr)
		#else:
		#	print("\t*** The deleter of the object with debuginfo='%s' has c_api==None, so unable to extFree() !" % debuginfo)


	def _initFromNull(self):
		self.__ptr = c_api.extFromNull()


	def _initFromInt(self, v):
		self.__ptr = c_api.extFromInt(v)


	def _initFromDouble(self, v):
		self.__ptr = c_api.extFromDouble(v)


	def _initFromString(self, v):
		self.__ptr = c_api.extFromString(ExtValue._cstringFromPython(v))


	@staticmethod
	def _makeNull():
		e = ExtValue(None, True)
		e._initFromNull()
		return e


	@staticmethod
	def _makeInt(v):
		e = ExtValue(None, True)
		e._initFromInt(v)
		return e


	@staticmethod
	def _makeDouble(v):
		e = ExtValue(None, True)
		e._initFromDouble(v)
		return e


	@staticmethod
	def _makeString(v):
		e = ExtValue(None, True)
		e._initFromString(v)
		return e


	@staticmethod
	def _rootObject():
		e = ExtValue(None, True)
		e.__ptr = c_api.rootObject()
		return e


	@staticmethod
	def _stringFromC(cptr):
		return cptr.decode(ExtValue._encoding)


	@staticmethod
	def _cstringFromPython(s):
		return ctypes.c_char_p(s.encode(ExtValue._encoding))


	def _type(self) -> int:
		return c_api.extType(self.__ptr)


	def _class(self) -> str | None:
		cls = c_api.extClass(self.__ptr)
		if cls is None:
			return None
		else:
			return ExtValue._stringFromC(cls)


	def _value(self) -> T:  # assumes the value returned will be of the same type as the argument when this object was constructed
		t = self._type()
		if t == 0:
			return None
		elif t == 1:
			return self._int()
		elif t == 2:
			return self._double()
		elif t == 3:
			return self._string()
		else:
			return self


	def _int(self) -> int:
		return c_api.extIntValue(self.__ptr)


	def _double(self) -> float:
		return c_api.extDoubleValue(self.__ptr)


	def _string(self) -> str:
		return ExtValue._stringFromC(c_api.extStringValue(self.__ptr))


	def _propCount(self) -> int:
		return c_api.extPropCount(self.__ptr)


	def _propFind(self, key) -> int:  # returns integer index of a property within an object. This index is an argument to a family of functions such as _propId(), _propName(), _propType() etc.
		return c_api.extPropFind(self.__ptr, ExtValue._cstringFromPython(key))


	def _propId(self, i) -> str:
		return ExtValue._stringFromC(c_api.extPropId(self.__ptr, i))


	def _propName(self, i) -> str:
		return ExtValue._stringFromC(c_api.extPropName(self.__ptr, i))


	def _propType(self, i) -> str:
		return ExtValue._stringFromC(c_api.extPropType(self.__ptr, i))


	def _propHelp(self, i) -> str:
		h = c_api.extPropHelp(self.__ptr, i)  # unlike other string fields, help is sometimes NULL
		return ExtValue._stringFromC(h) if h is not None else ''


	def _propFlags(self, i) -> int:
		return c_api.extPropFlags(self.__ptr, i)


	def _propGroup(self, i) -> int:
		return c_api.extPropGroup(self.__ptr, i)


	def _groupCount(self) -> int:
		return c_api.extGroupCount(self.__ptr)


	def _groupName(self, i) -> str:
		return ExtValue._stringFromC(c_api.extGroupName(self.__ptr, i))


	def _groupMember(self, g, i) -> int:
		return c_api.extGroupMember(self.__ptr, g, i)


	def _memberCount(self, g) -> int:
		return c_api.extMemberCount(self.__ptr, g)




	def __str__(self):
		return self._string()


	def __dir__(self):
		ids = dir(type(self))
		if self._type() == 4:
			for i in range(c_api.extPropCount(self.__ptr)):
				name = ExtValue._stringFromC(c_api.extPropId(self.__ptr, i))
				if name in ExtValue._reservedWords:
					name = 'x' + name
				ids.append(name)
		return ids


	def __getattr__(self, key):
		if key[0] == '_':  # handles our custom fields (starting with "_"); the other ones are Framsticks fields
			return self.__dict__[key]
		if key in ExtValue._reservedXWords:
			key = key[1:]
		prop_i = c_api.extPropFind(self.__ptr, ExtValue._cstringFromPython(key))
		if prop_i < 0:
			raise AttributeError("No '" + str(key) + "' in '" + str(self) + "'")
		t = ExtValue._stringFromC(c_api.extPropType(self.__ptr, prop_i))
		if t[0] == 'p':
			arg_types = ExtValue._reInsideParens.search(t)
			if arg_types:
				arg_types = arg_types.group(1).split(',')  # anyone wants to add argument type validation using param type declarations?


			def fun(*args):
				ext_args = []
				ext_pointers = []
				for a in args:
					if isinstance(a, ExtValue):
						ext = a
					else:
						ext = ExtValue(a)
					ext_args.append(ext)
					ext_pointers.append(ext.__ptr)
				ret = ExtValue(None, True)
				args_array = (ctypes.c_void_p * len(args))(*ext_pointers)
				ret.__ptr = c_api.extPropCall(self.__ptr, prop_i, len(args), args_array)
				return ret


			return fun
		else:
			ret = ExtValue(None, True)
			ret.__ptr = c_api.extPropGet(self.__ptr, prop_i)  # __setattr__() is called from here with key="_ExtValue__ptr"
			return ret


	def __setattr__(self, key, value):
		if key[0] == '_':  # handles setting our custom fields (starting with "_") and this includes "mangled private field names" like "__ptr" mangled to "_ExtValue__ptr"
			self.__dict__[key] = value
		else:  # Framsticks fields
			if key in ExtValue._reservedXWords:
				key = key[1:]
			prop_i = c_api.extPropFind(self.__ptr, ExtValue._cstringFromPython(key))
			if prop_i < 0:
				raise AttributeError("No '" + str(key) + "' in '" + str(self) + "'")
			if not isinstance(value, ExtValue):
				value = ExtValue(value)
			c_api.extPropSet(self.__ptr, prop_i, value.__ptr)


	def __getitem__(self, key):
		return self.get(key)


	def __setitem__(self, key, value):
		return self.set(key, value)


	def __len__(self) -> int:
		return self.size._int()


	def __iter__(self):
		class It:
			def __init__(self, container, frams_it):
				self.container = container
				self.frams_it = frams_it


			def __iter__(self):
				return self


			def __next__(self):
				if self.frams_it.next._int() != 0:
					return self.frams_it.value
				else:
					raise StopIteration()

		return It(self, self.iterator)


if __name__ == "__main__":
	print('This is a utility module. For sample usage, see "frams-test.py".')
