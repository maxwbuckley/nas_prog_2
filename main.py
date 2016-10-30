#! /usr/bin/python3
""" Docstring. FILL OUT"""
from proto_genfiles.protos import sor_pb2


def VectorProtoExample():
  vector_b = sor_pb2.Vector(vector_name="b")
  vector_b.length = 3
  for i in range(3, 6):
    vector_b.values.append(i)
  return vector_b

def MatrixProtoExample():
  matrix_a = sor_pb2.SparseMatrix(matrix_name="a")
  matrix_a.row_count = 3
  matrix_a.column_count = 3
  for i in range(0, 3):
    # This creates and returns a pointer to a sor_pb2.SparseValue message.
    value = matrix_a.values.add()
    value.row_index = i
    value.column_index = i
    value.value = (i + 1) * 3.9
  return matrix_a

vector_b = VectorProtoExample()
matrix_a = MatrixProtoExample()
print(vector_b)
print(matrix_a)
