#! /usr/bin/python3
"""Example code for using protos."""
from proto_genfiles.protos import sor_pb2


def VectorProtoExample():
  """Create an example Vector proto."""
  vector_b = sor_pb2.Vector(vector_name="b", length=3)
  for i in range(3, 6):
    vector_b.values.append(i)
  return vector_b

def SparseMatrixProtoExample():
  """Create an example SparseMarix proto."""
  matrix_a = sor_pb2.SparseMatrix(
      matrix_name="a", row_count=3, column_count=3)
  for i in range(0, 3):
    # This creates and returns a pointer to a sor_pb2.SparseValue message.
    value = matrix_a.values.add()
    value.row_index = i
    value.column_index = i
    # This is just a made up float value.
    value.value = (i + 1) * 3.9
  return matrix_a

vector_b = VectorProtoExample()
matrix_a = SparseMatrixProtoExample()
print("")
# This is just the default printing behavior for a proto.
print(vector_b)
print(matrix_a)
