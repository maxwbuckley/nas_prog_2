"""Library for use in input and output of program."""
from proto_genfiles.protos import sor_pb2

def read_input(filename):
  """Reads input.
  
  Args:
    filename: The string filename.
  Returns:
    tuple of sor_pb2.SparseMatrix A and sor_pb2.Vector b.
  Raises:
    IOError. If the file cannot be opened or does not exist.
  """
  pass

def write_output(filename, output_message):
  """Writes output file
  Args:
    filename: The string filename.
    output_message: A sor_pb2.SorReturnValue
  Raises:
    IOError. If the file cannot be opened or written.
  """
  pass
