"""Class and methods for working with Vectors."""
import validation
from proto_genfiles.protos import sor_pb2

class Vector(object):
  def __init__(self, name=None, number_list=None,  vector_proto=None):
    """Create a new vector object from the received vector proto.
  
    Args:
      vector_proto: A sor_pb2.Vector proto.
    Raises:
      validation.ValidationError if the proto is invalid.
    """
    if number_list and vector_proto:
      raise Exception("Don't specify both")
    elif vector_proto is not None:
      self._fromProto(vector_proto)
    elif number_list is not None:
      self._fromNumberList(name, number_list)
    else:
      raise Exception("Must specify at least one")
  
  def _fromNumberList(self, name, number_list):
    """Create a new vector object from the received vector proto.
  
    Args:
      name: a string name for the vector
      number_list: a list of numbers either floats or integers.
    Raises:
      validation.ValidationError if there are non numbers passed.
    """
    validation.ValidateNumberList(number_list)
    self._name = name
    self._values = number_list
    self._length = len(self.values)

  
  def _fromProto(self, vector_proto):
    """Create a new vector object from the received vector proto.
  
    Args:
      vector_proto: A sor_pb2.Vector proto.
    Raises:
      validation.ValidationError if the proto is invalid.
    """
    validation.ValidateVectorProto(vector_proto)
    self._name = vector_proto.vector_name
    self._values = vector_proto.values
    # This was verified above.
    self._length = len(self.values)
    
 
  def toProto(self):
    """Converts Vector object to sor_pb2.Vector object
    
    Returns:
      A sor_pb2.Vector proto object.
    """
    vector_proto = sor_pb2.Vector(
        vector_name=self._name, length=self._length)
    vector_proto.values.extend(self._values)
    return vector_proto 
