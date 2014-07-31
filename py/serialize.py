
import functools

def Serialized(method_or_lock_name):
  """A decorator for a function or method that puts a lock around it.

     The signature for this is complicated, for notational convenience, and also
     because python's decorator protocol is complicated.  There are two cases:

     class A(object):
       @Serialized
       def M(...) -> Look in the instance of A for a 'lock' attribute, and lock
         that around calls to M.  Useful to mean "serialized wrt the object".

     class B(object):
       @Serialized('lock_name')
       def M(...) -> Like the above, except look for a 'lock_name' attribute
         in the first argument (self).  Useful to mean "serialized wrt reentrant
         calls of M" if you give it a lock specific to M.

     Args:
       method_or_lock_name: str | callable to serialize

     Returns:
       serialized version of the method.
  """
  if isinstance(method_or_lock_name, str):
    # @Serialized('lock_name') means its a method and look in self for
    # 'lock_name'
      return lambda method: _SerializedMethod(method, method_or_lock_name)
    else:
    # must be a callable
    # plain call to @Serialized means look in self for 'lock'
      return _SerializedMethod(method_or_lock_name, 'lock')


def SerializedWith(lock):
  """
  Decorator to serialize a function when the lock object is already in scope.

  Serialize plain functions, or methods where the lock has a static scope
  (e.g., module-level).

  Args:
    lock: the lock (not its name) used to serialize calls to the function

  Returns:
    Serialized version of the decorated function.
  """
  return lambda func: SerializedFunction(func, lock)
