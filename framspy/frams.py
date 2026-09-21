"""
Framsticks as a Python module.

Static FramScript objects are available inside this module under their well-known names
(frams.Simulator, frams.GenePools, etc.)

These objects and all values passed to and from Framsticks are instances of ``frams_extvalue.ExtValue`` class.
Python values are automatically converted to Framsticks data types.
Use ExtValue._makeInt()/_makeDouble()/_makeString()/_makeNull() for explicit conversions.
Simple values returned from Framsticks can be converted to their natural Python
counterparts using ``_value()``, or forced to a specific type with ``_int()``/``_double()``/``_string()``.

All non-Framsticks Python attributes start with '_' to avoid conflicts with Framsticks attributes.
Framsticks names that are Python reserved words are prefixed with 'x' (currently just Simulator.ximport).

For sample usage, see ``frams-test.py`` and ``FramsticksLib.py``.

If you want to run many independent instances of this class in parallel, use the "multiprocessing" module and then each process
that uses this module will initialize it and get access to a separate instance of the Framsticks library.

If you want to use this module from multiple threads concurrently, use the "-t" option for ``init()``.
This will make concurrent calls from different threads sequential, thus making them safe.
However, this will likely degrade performance (due to required locking) compared to the single-threaded use.

For interfaces in other languages (e.g., using the Framsticks library in your C++ code), see ``../cpp/frams/frams-objects.h``
"""

import ctypes, sys, os

import frams_extvalue
from frams_extvalue import ExtValue


def init(*args):
	"""
	Initializes the connection to Framsticks dll/so/dylib.

	Python programs do not have to know the Framsticks path but if they know, just pass the path as the first argument.
	Similarly, '-dPATH' and '-DPATH' needed by Framsticks are optional and derived from the first path, unless they are specified as args in init().
	'-LNAME' is the optional library name (full name including the file name extension), default is 'frams-objects.dll/.so/.dylib' depending on the platform.
	All other arguments are passed to Framsticks and are not interpreted by this function.
	"""

	frams_d = None
	frams_D = None
	lib_path = None
	lib_name = ('frams-objects.dylib' if sys.platform == 'darwin' else 'frams-objects.so') if os.name == 'posix' else 'frams-objects.dll'
	initargs = []
	for a in args:
		if a[:2] == '-d':
			frams_d = a
		elif a[:2] == '-D':
			frams_D = a
		elif a[:2] == '-L':
			lib_name = a[2:]
		elif a[:2] == '-t':
			print("frams.py: thread synchronization enabled.")  # Due to performance penalty, only use if you are really calling methods from different threads.
			from functools import wraps
			from threading import RLock
			
			def threads_synchronized(lock):
				def wrapper(f):
					@wraps(f)
					def inner_wrapper(*args, **kwargs):
						with lock:
							return f(*args, **kwargs)
					return inner_wrapper
				return wrapper

			thread_synchronizer = threads_synchronized(RLock())
			for name in ExtValue.__dict__:
				attr = getattr(ExtValue, name)
				if callable(attr) and attr:  # decorate all methods of ExtValue with a reentrant lock so that different threads do not use them concurrently
					setattr(ExtValue, name, thread_synchronizer(attr))
		elif lib_path is None:
			lib_path = a
		else:
			initargs.append(a)
	if lib_path is None:
		# TODO: use environment variable and/or the zip distribution we are in when the path is not specified in arg.
		# For now, just assume the current dir is Framsticks.
		lib_path = '.'

	if os.name == 'nt':
		if sys.version_info < (3, 8):
			original_dir = os.getcwd()
			os.chdir(lib_path)  # because under Windows, frams-objects.dll requires other dll's which reside in the same directory, so we must change current dir for them to be found while loading the main dll.
		else:
			os.add_dll_directory(os.path.abspath(lib_path))
	abs_data = os.path.join(os.path.abspath(lib_path), "data")  # use absolute path for -d and -D so python is free to cd anywhere without confusing Framsticks

	# for the hypothetical case without lib_path, the abs_data must be obtained from somewhere else
	if frams_d is None:
		frams_d = '-d' + abs_data
	if frams_D is None:
		frams_D = '-D' + abs_data
	initargs.insert(0, frams_d)
	initargs.insert(0, frams_D)
	initargs.insert(0, 'dummy.exe')  # as an offset, 0th arg is by convention the app name

	if lib_path is not None:  # theoretically, this should only be needed for "and os.name == 'posix'", but in windows python 3.9.5, without using the full lib_name path, there is FileNotFoundError: Could not find module 'frams-objects.dll' (or one of its dependencies). Try using the full path with constructor syntax. Maybe related: https://bugs.python.org/issue42114 and https://stackoverflow.com/questions/59330863/cant-import-dll-module-in-python and https://bugs.python.org/issue39393
		lib_name = os.path.join(lib_path, lib_name)  # lib_path is always set ('.' when not specified). For the (currently unused) case of lib_path==None, the resulting lib_name is a bare filename without any path, which loads the library from a system-configured location.
	try:
		frams_extvalue.c_api = ctypes.CDLL(lib_name)  # if accessing this module from multiple threads, they will all share a single c_api and access the same copy of the library and its data. If you want separate independent copies, read the comment at the top of this file on using the "multiprocessing" module.
	except OSError as e:
		print("*** Could not find or open '%s' from '%s'.\n*** Did you provide proper arguments and is that file readable?\n" % (lib_name, os.getcwd()))
		raise

	if os.name == 'nt' and sys.version_info < (3, 8):
		os.chdir(original_dir)  # restore current working dir after loading the library so Framsticks sees the expected directory

	frams_extvalue.c_api.init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
	frams_extvalue.c_api.init.restype = None
	frams_extvalue.c_api.extFree.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extFree.restype = None
	frams_extvalue.c_api.extType.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extType.restype = ctypes.c_int
	frams_extvalue.c_api.extFromNull.argtypes = []
	frams_extvalue.c_api.extFromNull.restype = ctypes.c_void_p
	frams_extvalue.c_api.extFromInt.argtypes = [ctypes.c_int]
	frams_extvalue.c_api.extFromInt.restype = ctypes.c_void_p
	frams_extvalue.c_api.extFromDouble.argtypes = [ctypes.c_double]
	frams_extvalue.c_api.extFromDouble.restype = ctypes.c_void_p
	frams_extvalue.c_api.extFromString.argtypes = [ctypes.c_char_p]
	frams_extvalue.c_api.extFromString.restype = ctypes.c_void_p
	frams_extvalue.c_api.extIntValue.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extIntValue.restype = ctypes.c_int
	frams_extvalue.c_api.extDoubleValue.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extDoubleValue.restype = ctypes.c_double
	frams_extvalue.c_api.extStringValue.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extStringValue.restype = ctypes.c_char_p
	frams_extvalue.c_api.extClass.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extClass.restype = ctypes.c_char_p
	frams_extvalue.c_api.extPropCount.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extPropCount.restype = ctypes.c_int
	frams_extvalue.c_api.extPropId.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropId.restype = ctypes.c_char_p
	frams_extvalue.c_api.extPropName.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropName.restype = ctypes.c_char_p
	frams_extvalue.c_api.extPropType.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropType.restype = ctypes.c_char_p
	frams_extvalue.c_api.extPropGroup.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropGroup.restype = ctypes.c_int
	frams_extvalue.c_api.extPropFlags.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropFlags.restype = ctypes.c_int
	frams_extvalue.c_api.extPropHelp.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropHelp.restype = ctypes.c_char_p
	frams_extvalue.c_api.extPropFind.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
	frams_extvalue.c_api.extPropFind.restype = ctypes.c_int
	frams_extvalue.c_api.extPropGet.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extPropGet.restype = ctypes.c_void_p
	frams_extvalue.c_api.extPropSet.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
	frams_extvalue.c_api.extPropSet.restype = ctypes.c_int
	frams_extvalue.c_api.extPropCall.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
	frams_extvalue.c_api.extPropCall.restype = ctypes.c_void_p
	frams_extvalue.c_api.extGroupCount.argtypes = [ctypes.c_void_p]
	frams_extvalue.c_api.extGroupCount.restype = ctypes.c_int
	frams_extvalue.c_api.extGroupName.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extGroupName.restype = ctypes.c_char_p
	frams_extvalue.c_api.extGroupMember.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
	frams_extvalue.c_api.extGroupMember.restype = ctypes.c_int
	frams_extvalue.c_api.extMemberCount.argtypes = [ctypes.c_void_p, ctypes.c_int]
	frams_extvalue.c_api.extMemberCount.restype = ctypes.c_int
	frams_extvalue.c_api.rootObject.argtypes = []
	frams_extvalue.c_api.rootObject.restype = ctypes.c_void_p

	c_args = (ctypes.c_char_p * len(initargs))(*list(a.encode(ExtValue._encoding) for a in initargs))
	frams_extvalue.c_api.init(len(initargs), c_args)

	# create the first level of hierarchy of Framsticks objects (copying from Framsticks' _rootObject() to Python's frams module), so the hierarchy has one level less (Python's frams becomes the root) and thus the access path to Framsticks objects is shorter (frams.path... instead of frams.root.path...)
	Root = ExtValue._rootObject()
	for n in dir(Root):
		if n[0].isalpha():
			attr = getattr(Root, n)
			if isinstance(attr, ExtValue):
				attr = attr._value()
			setattr(sys.modules[__name__], n, attr)

	print('Using Framsticks version: ' + str(Simulator.version_string))
	print('Home (writable) dir     : ' + home_dir)
	print('Resources dir           : ' + res_dir)
	print()


if __name__ == "__main__":
	print('This is a utility module, meant to be imported. For sample usage, see "frams-test.py".')
