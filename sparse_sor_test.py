#! /usr/bin/python3
"""Unit tests associated with sparse_matrix.py."""
import vector
import sparse_sor
import sparse_matrix
from proto_genfiles.protos import sor_pb2
import unittest

def almost_equal(value_1, value_2, accuracy = 10**-2):
  return abs(value_1 - value_2) < accuracy

class SparseSorSolverTest(unittest.TestCase):

  def setUp(self):
    self.matrix_a = sparse_matrix.SparseMatrix(dense_matrix=
        [[7, 1, 0],
         [1, -7, 1],
         [0, 1, 8]])

    self.positive_definite_symmetric = sparse_matrix.SparseMatrix(dense_matrix=
        [[2, -1, 0],
         [-1, 2, -1],
         [0, -1, 2]])
    self.vector_b = vector.Vector(name="b", number_list=[1, 1, 1])

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

  # Class example with differing levels of relaxation
  def testSparseSorSolver_ClassExampleRelaxationNormal(self):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.matrix_a, self.vector_b, 10, 10**-20, 1.0)
    print(sparse_sor_solver)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)

  def testSparseSorSolver_ClassExampleRelaxationHigh(self):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.matrix_a, self.vector_b, 10, 10**-20, 1.5)
    print(sparse_sor_solver)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)

  def testSparseSorSolver_ClassExample2RelaxationVeryHigh(self):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.matrix_a, self.vector_b, 50, 10**-20, 1.9, True)
    print(sparse_sor_solver)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.X_SEQUENCE_DIVERGENCE)

  # Positive definite symmetric example with differing levels of relaxation
  def testSparseSorSolver_PositiveDefiniteRelaxationNormal(self):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.positive_definite_symmetric, self.vector_b, 25, 10**-20, 1.0, True)
    print(sparse_sor_solver)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)

  def testSparseSorSolver_PositiveDefiniteRelaxationHigh(self):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.positive_definite_symmetric, self.vector_b, 25, 10**-20, 1.5, True)
    print(sparse_sor_solver)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)

  def testSparseSorSolver_PositiveDefiniteRelaxationVeryHigh(self):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.positive_definite_symmetric, self.vector_b, 25, 10**-20, 1.9, True)
    print(sparse_sor_solver)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)


  def testSparseSorSolver_DivergenceExampleHighRelaxationRate(self):
    vector_b = vector.Vector(name="b", number_list=[-1, 7, -7])

    sparse_sor_solver = sparse_sor.SparseSorSolver(
        self.matrix_a, vector_b, 100, .0001, 30.0)

    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.X_SEQUENCE_DIVERGENCE)

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

  def testSparseSorSolverToProto(self):
    matrix_a = sparse_matrix.SparseMatrix(dense_matrix=
        [[3, -1, 1],
         [-1, 3, -1],
         [1, -1, 3]])

    vector_b = vector.Vector(name="b", number_list=[-1, 7, -7])

    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix_a, vector_b, 10, .0001, 1.0)
    solution_proto = sparse_sor_solver.to_proto()

  def testIllConditionedHigh(self):
    matrix_ill_conditioned = sparse_matrix.SparseMatrix(dense_matrix=
          [[1.01, 1],
           [1, 1.01]])

    vector_ill_conditioned = vector.Vector(name = "b", number_list = [2, 2])

    sparse_sor_solver = sparse_sor.SparseSorSolver(
            matrix_ill_conditioned, vector_ill_conditioned,
            50, 10**-20, 1.5, True)

    print(sparse_sor_solver)

  def testZeroOnDiagonal(self):
    zero_diagonal_mat = sparse_matrix.SparseMatrix(dense_matrix=
          [[4, 1],
           [1, 0]])
    b_vector = vector.Vector(name = "b", number_list = [2, 2])
    sparse_sor_solver = sparse_sor.SparseSorSolver(
            zero_diagonal_mat, b_vector,
            50, 10**-20, 1)
    self.assertEqual(sparse_sor_solver.stopping_reason,
                     sor_pb2.SorReturnValue.ZERO_ON_DIAGONAL)

if __name__ == '__main__':
  unittest.main()
