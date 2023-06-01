from typing import (
	Any,
	Dict,
	Callable,
	List,
	Mapping,
	Optional,
	OrderedDict,
	Tuple,
	TypeVar,
	Union
)

from threading import Lock

Handler = TypeVar("Handler", bound=Callable)

class EventEmitter:
	def __init__(self) -> None:
		self.__callbacks__: Dict[str, "OrderedDict[Callable, Callable]"] = {}
		self.__lock__: Lock = Lock()
		
	def __getstate__(self) -> Mapping[str, Any]:
		state = self.__dict__.copy()
		del state["__lock__"]
		return state
	
	def __setstate__(self, state: Mapping[str, Any]) -> None:
		self.__dict__.update(state)
		self.__lock__ = Lock()

	def __handle_error__(self, event: str, error) -> None:
		if event == "error":
			if isinstance(error, Exception): raise error
			else: raise Exception(f"Uncaught 'error' event: {error}")

	def __emit__(self, callback: Callable, *args, **kwargs):
		ret = callback(*args, **kwargs)
		return ret
	
	def __call_handlers__(self, event, *args, **kwargs) -> bool:
		handled = False

		with self.__lock__:
			fns = list(self.__callbacks__.get(event, OrderedDict()).value())
		for fn in fns:
			self.__emit__(fn, *args, **kwargs)
			handled = True
		
		return handled
	
	def __add_handler__(self, event: str, key: Union[str, Handler], callback: Handler):
		with self.__lock__:
			if event not in self.__callbacks__:
				self.__callbacks__[event] = OrderedDict()
			self.__callbacks__[event][key] = callback

		return self
	
	def __remove_handler__(self, event: str, callback: Callable):
		self.__callbacks__[event].pop(callback)
		if not len(self.__callbacks__[event]):
			del self.__callbacks__[event]
	
	def on(self, event: str, callback: Callable):
		return self.__add_handler__(event, callback, callback)
	
	def emit(self, event, *args, **kwargs):
		handled = self.__call_handlers__(event, *args, **kwargs)

		if not handled:
			self.__handle_error__(event, args[0] if args else None)
		
		return handled
	
	def once(self, event: str, callback: Handler):
		def wrapper(fn: Handler):
			def inner(*args, **kwargs):
				with self.__lock__:
					if event in self.__callbacks__ and fn in self.__callbacks__[event]:
						self.off(event, fn)
					else: return None

				return fn(*args, **args)
			
			self.__add_handler__(event, fn, inner)
			return fn
		
		return wrapper(callback)
	
	def off(self, event: Optional[str], callback: Optional[Callable]):
		with self.__lock__:
			if event is not None:
				if callback is not None:
					self.__remove_handler__(event, callback)
				else:
					self.__callbacks__[event] = OrderedDict()
			else:
				self.__callbacks__ = {}