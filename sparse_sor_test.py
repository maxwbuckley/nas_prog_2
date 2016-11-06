#! /usr/bin/python3
"""Unit tests associated with sparse_matrix.py."""
import vector
import sparse_sor
import sparse_matrix
from proto_genfiles.protos import sor_pb2
import unittest

def almost_equal(value_1, value_2, accuracy = 10**4):
  return abs(value_1 - value_2) < accuracy

class SparseSorSolverTest(unittest.TestCase):

  def testSparseSorSolver_MatrixProto(self):
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

    vector_b = vector.Vector(name="b", number_list=[2, 3, 4])

    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix_a, vector_b, 10, .0001, 1.0)
    print(sparse_sor_solver)
  
  def testSparseSorSolver_ClassExample(self):
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=
        [[7, 1, 0],
         [1, -7, 1],
         [0, 1, 8]])

    vector_b = vector.Vector(name="b", number_list=[1, 1, 1])

    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix_a, vector_b, 10, .0001, 1.25)
    print(sparse_sor_solver)  
  
  def testSparseSorSolver_SolvedExample(self):
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=
        [[3, -1, 1],
         [-1, 3, -1],
         [1, -1, 3]])

    vector_b = vector.Vector(name="b", number_list=[-1, 7, -7])

    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix_a, vector_b, 10, .0001, 1.0)
    
    expected = [1, 2, -2]
    
    self.assertTrue(all(
      almost_equal(*values) for values in zip(expected, sparse_sor_solver.x)))

if __name__ == '__main__':
  unittest.main() 
