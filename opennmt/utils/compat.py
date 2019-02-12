"""Functions for compatibility with different TensorFlow versions."""

import tensorflow as tf


def is_tf2():
  """Returns ``True`` if running TensorFlow 2.0."""
  return tf.__version__.startswith("2")

def tf_supports(symbol):
  """Returns ``True`` if TensorFlow defines :obj:`symbol`."""
  return _string_to_tf_symbol(symbol) is not None

def tf_compat(v2=None, v1=None):  # pylint: disable=invalid-name
  """Returns the compatible symbol based on the current TensorFlow version.

  Args:
    v2: The candidate v2 symbol name.
    v1: The candidate v1 symbol name.

  Returns:
    A TensorFlow symbol.

  Raises:
    ValueError: if no symbol can be found.
  """
  candidates = []
  if v2 is not None:
    candidates.append(v2)
  if v1 is not None:
    candidates.append(v1)
    candidates.append("compat.v1.%s" % v1)
  for candidate in candidates:
    symbol = _string_to_tf_symbol(candidate)
    if symbol is not None:
      return symbol
  raise ValueError("Failure to resolve the TensorFlow symbol")

def _string_to_tf_symbol(symbol):
  modules = symbol.split(".")
  namespace = tf
  for module in modules:
    namespace = getattr(namespace, module, None)
    if namespace is None:
      return None
  return namespace


# pylint: disable=invalid-name
gfile_copy = tf_compat(v2="io.gfile.copy", v1="gfile.Copy")
gfile_exists = tf_compat(v2="io.gfile.exists", v1="gfile.Exists")
gfile_open = tf_compat(v2="io.gfile.GFile", v1="gfile.GFile")
is_tensor = tf_compat(v2="is_tensor", v1="contrib.framework.is_tensor")
logging = tf_compat(v1="logging")
nest = tf_compat(v2="nest", v1="contrib.framework.nest")
