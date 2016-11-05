#! /usr/bin/python3
"""Unit tests associated with sparse_matrix.py."""
import sparse_matrix
from proto_genfiles.protos import sor_pb2
import unittest
import validation

class SparseMatrixTest(unittest.TestCase):

  def testSparseMatrix_FromProto(self):
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

    self.assertEqual(expected, matrix_a.to_dense_matrix())
    self.assertEqual([0, 1, 2, 3], matrix_a.rowStart)
    self.assertEqual([0, 1, 2], matrix_a.cols)
    self.assertEqual([3.9, 7.8, 11.7], matrix_a.vals)

  def testSparseMatrix_FromDenseMatrix(self):
    matrix_a_proto = sor_pb2.SparseMatrix(
        matrix_name="a", row_count=3, column_count=3)
    expected = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=expected)

    self.assertEqual(expected, matrix_a.to_dense_matrix())
    self.assertEqual([0, 2, 3, 5], matrix_a.rowStart)
    self.assertEqual([0, 2, 1, 0, 2], matrix_a.cols)
    self.assertEqual([1, 1, 1, 1, 1], matrix_a.vals)
    
    expected = [[9, 7, 16],
                [0, 7.8, 0],
                [0, 0, 11.7]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=expected)


    self.assertEqual([0, 3, 4, 5], matrix_a.rowStart)
    self.assertEqual([0, 1, 2, 1, 2], matrix_a.cols)
    self.assertEqual([9, 7, 16, 7.8, 11.7], matrix_a.vals)
    self.assertEqual(expected, matrix_a.to_dense_matrix())

  def testSparseMatrix_EmptyRows(self):
    expected = [[1, 0, 0],
                [0, 0, 0],
                [0, 0, 1]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=expected)


    self.assertEqual([0, 1, 1, 2], matrix_a.rowStart)
    self.assertEqual([0, 2], matrix_a.cols)
    self.assertEqual([1, 1], matrix_a.vals)
    self.assertEqual(expected, matrix_a.to_dense_matrix())

  def testSparseMatrix_BigSquareMatrix(self):
    expected = [[9.1, 0, 0, 0, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 5, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 1, 1, 1]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=expected)


    self.assertEqual([0, 2, 3, 4, 5, 10], matrix_a.rowStart)
    self.assertEqual([0, 4, 2, 2, 2, 0, 1, 2, 3, 4], matrix_a.cols)
    self.assertEqual([9.1, 1, 1, 5, 1, 1, 1, 1, 1, 1], matrix_a.vals)
    self.assertEqual(expected, matrix_a.to_dense_matrix())

  def testSparseMatrix_BigSquareMatrixEmptyRows(self):
    expected = [[1, 0, 0, 0, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 1, 1, 1]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=expected)


    self.assertEqual([0, 2, 3, 3, 4, 9], matrix_a.rowStart)
    self.assertEqual([0, 4, 2, 2, 0, 1, 2, 3, 4], matrix_a.cols)
    self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1], matrix_a.vals)
    self.assertEqual(expected, matrix_a.to_dense_matrix())
  

  def testSparseMatrix_ProtosSetup_InvalidColumnCount(self):
    matrix_a_proto = sor_pb2.SparseMatrix(
      matrix_name='a', row_count=3, column_count=3)
    for i in range(0, 4):
      value = matrix_a_proto.values.add()
      value.row_index = i
      value.column_index = i
      value.value = (i + 1) * 2
    
    self.assertRaises(validation.ValidationError,
                      validation.ValidateSparseMatrixProto, matrix_a_proto)

  def testSparseMatrixIsSquareMatrix_True(self):
    square_mat = [[8, 1, -1],
                  [2, 9, -3],
                  [1, -8, 10]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=square_mat)
    self.assertTrue(matrix_a.is_square_matrix())
  
  def testSparseMatrixIsSquareMatrix_False(self):
    non_square_mat = [[8, 1, -1, 0],
                      [2, 9, -3, 9],
                      [1, -8, 10, 0]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=non_square_mat)
    self.assertFalse(matrix_a.is_square_matrix())

  def testSparseMatrixIsStrictlyRowDiagonallyDominant_Success(self):
    dd_mat = [[8, 1, -1],
              [2, 9, -3],
              [1, -8, 10]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=dd_mat)
    self.assertTrue(matrix_a.is_strictly_row_diagonally_dominant())
  
  def testSparseMatrixIsStrictlyRowDiagonallyDominant_FailureNonDominant(self):
    non_dd_mat = [[8, 1, -10],
                  [12, 9, -3],
                  [1, -8, 10]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=non_dd_mat)
    self.assertFalse(matrix_a.is_strictly_row_diagonally_dominant())
  
  def testSparseMatrixIsStrictlyRowDiagonallyDominant_FailureNonSquare(self):
    non_square_mat = [[8, 1, -1, 1],
                      [2, 9, -3, 1],
                      [1, -8, 10, 1]]
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=non_square_mat)
    self.assertFalse(matrix_a.is_strictly_row_diagonally_dominant())

if __name__ == '__main__':
  unittest.main() 
