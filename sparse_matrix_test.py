#! /usr/bin/python3
"""Unit tests associated with sparse_matrix.py."""
import sparse_matrix
from proto_genfiles.protos import sor_pb2
import unittest

class SparseMatrixTest(unittest.TestCase):

  def testSparseMatrixSetup(self):
    matrix_a_proto = sor_pb2.SparseMatrix(
        matrix_name="a", row_count=3, column_count=3)
    for i in range(0, 3):
      # This creates and returns a pointer to a sor_pb2.SparseValue message.
      value = matrix_a_proto.values.add()
      value.row_index = i
      value.column_index = i
      # This is just a made up float value.
      value.value = (i + 1) * 3.9

    matrix_a = sparse_matrix.SparseMatrix(matrix_a_proto)

    expected = [[3.9, 0, 0],[0, 7.8, 0],[0, 0, 11.7]]
    print(matrix_a)

    self.assertEqual(expected, matrix_a.to_dense_matrix())
    self.assertEqual([0, 1, 2, 3], matrix_a.rowStart)
    self.assertEqual([0, 1, 2], matrix_a.cols)
    self.assertEqual([3.9, 7.8, 11.7], matrix_a.vals)

  def testSparseMatrixSquare(self):
    matrix_a_proto = sor_pb2.SparseMatrix(
        matrix_name="a", row_count=3, column_count=3)
    values = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    for i in range(0, 3):
      for j in range(0, 3):
        # This creates and returns a pointer to a sor_pb2.SparseValue message.
        value = matrix_a_proto.values.add()
        value.row_index = i
        value.column_index = j
      # This is just a made up float value.
        value.value = values[i][j]

    matrix_a = sparse_matrix.SparseMatrix(matrix_a_proto)

    expected = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    print(matrix_a)

    self.assertEqual(expected, matrix_a.to_dense_matrix())
    self.assertEqual([0, 0, 2, 2, 3], matrix_a.rowStart)
    self.assertEqual([0, 1, 2], matrix_a.cols)
    self.assertEqual([1, 1, 1, 1], matrix_a.vals)


if __name__ == '__main__':
  unittest.main() 
