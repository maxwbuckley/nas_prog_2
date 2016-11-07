"""Library for use in input and output of program."""
from proto_genfiles.protos import sor_pb2
import re

def _read_file(filename):
  """Reads input file.

  Args:
    filename: The string filename.
  Returns:
    string filecontents.
  Raises:
    IOError. If the file cannot be opened or does not exist.
  """
  try:
    file_obj = open(filename, 'r')
    file_contents = file_obj.read()
  finally:
    file_obj.close()
  return file_contents


def read_input(filename='nas_Sor.in'):
  """Reads input.

  Args:
    filename: The string filename.
  Returns:
    tuple of sor_pb2.SparseMatrix A and sor_pb2.Vector b.
  Raises:
    IOError. If the file cannot be opened or does not exist.
  """
  file_contents = _read_file(filename)
  values = file_contents.split('\n\n')
  string_matrix = values[0]
  string_vector = values[1]
  matrix_proto = _process_string_matrix_proto(string_matrix)
  vector_proto = _process_string_vector_proto(string_vector)
  return (matrix_proto, vector_proto)


def _process_string_vector_proto(string_vector_proto):
  string_segments = string_vector_proto.split('values: ')
  head_segment = string_segments[0]
  name = re.search(r'vector_name: "([^"]+)"', head_segment).group(1)
  length = re.search(r'length: (\d+)', head_segment).group(1)
  vector_proto = sor_pb2.Vector(vector_name=name, length=int(length))
  for value in string_segments[1:]:
    vector_proto.values.append(float(value.strip()))
  return vector_proto


def _process_string_matrix_proto(string_matrix_proto):
  string_segments = string_matrix_proto.split('values ')
  head_segment = string_segments[0]
  name = re.search(r'matrix_name: "([^"]+)"', head_segment).group(1)
  rows = re.search(r'row_count: (\d+)', head_segment).group(1)
  columns = re.search(r'column_count: (\d+)', head_segment).group(1)
  sparse_matrix_proto = sor_pb2.SparseMatrix(
      matrix_name=name, row_count=int(rows), column_count=int(columns))
  for segment in string_segments[1:]:
    sparse_value = sparse_matrix_proto.values.add()
    row_index = re.search(r'row_index: (\d+)', segment)
    column_index = re.search(r'column_index: (\d+)', segment)
    value = re.search(r'value: (-?[\d.]+)', segment).group(1)
    if row_index:
      sparse_value.row_index = int(row_index.group(1))
    if column_index:
      sparse_value.column_index = int(row_index.group(1))
    sparse_value.value = float(value)
  return sparse_matrix_proto


def write_output(filename, output_message):
  """Writes output file
  Args:
    filename: The string filename.
    output_message: A sor_pb2.SorReturnValue
  Raises:
    IOError. If the file cannot be opened or written.
  """
  pass
