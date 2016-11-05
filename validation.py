"""Validation libraries for testing assumptions."""
import proto_genfiles.protos.sor_pb2
import numbers

class ValidationError(Exception):
  """If the data is invalid"""

def ValidateVectorProto(vector_proto):
  """Check if the Vector proto is consistent

  Args:
    vector_proto: A sor_pb2.Vector.
  Returns:
    True if the input is valid.
  Raises:
    ValidationError if the input is invalid.
  """
  if vector_proto.length == len(vector_proto.values):
    return True
  raise ValidationError("Vector proto is invalid. Length does not match "
                        "number of elements")


def ValidateSparseMatrixProto(sparse_matrix_proto):
  """Check if the SparseMatrix proto is consistent
  
  Args:
    sparse_matrix_proto: A sor_pb2.SparseMatrix.
  Returns:
    True if the input is valid.
  Raises:
    ValidationError if the input is invalid.
  """
  max_rows = sparse_matrix_proto.row_count
  max_columns = sparse_matrix_proto.column_count
  collision_grid = [
      [False for _ in range(max_columns)] for _ in range(max_rows)]
  if len(sparse_matrix_proto.values) > max_rows * max_columns:
    raise ValidationError("Too many values present in sparse matrix proto")
  for value in sparse_matrix_proto.values:
    if value.column_index >= max_columns or value.row_index >= max_rows:
      raise ValidationError("Row or column index out of bounds")
    # Need to check collisions. I.e. two or more values writing to same cell.
    if collision_grid[value.row_index][value.column_index]:
      raise ValidationError("Duplicate values written to one cell")
    else:
      # Set the value for this cell to seen.
      collision_grid[value.row_index][value.column_index] = True
  return True

def ValidateNumberList(number_list):
  """Describe"""
  if all([isinstance(number, numbers.Number) for number in number_list]):
    return True  
  raise ValidationError("Non numbers passed in list")
