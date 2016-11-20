#! /usr/bin/python3 
"""This script is to experiment with different relaxation rates on a very large
matrix."""
import sparse_matrix
import vector
import sparse_sor
import pandas
from proto_genfiles.protos import sor_pb2
import random
from matplotlib import pyplot


def effect_relaxation_rate(
    matrix, vector, maxits=50):
  """Calculate stopping iterationa matrix with different relaxation rates.

  Args:
    matrix: A sparse_matrix.Matrix. This needs to be diagonally dominant.
    vector: A vector.Vector
    maxits: Max number of iterations

  Returns: List of sum of residuals for different relaxation rates.
  """
  i = 0.1
  results = []
  while(i < 2.1):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix, vector, maxits, 2**-20, i)
    results.append(sparse_sor_solver.iteration)
    i += 0.1
  return(results)
 
index_list = [ x / 10 for x in range(1,21)]

# Experiment to see effect of very large matrix 
print("--------------------------------------------------------------------")
print("Experiment with large, randomly generated diagonally dominant matrix")
print("--------------------------------------------------------------------")

# Create tridiagonal matrix
matrix_a_proto = sor_pb2.SparseMatrix(
    matrix_name="a", row_count=5000, column_count=5000)
for i in range(0, 5000):
  value = matrix_a_proto.values.add()
  value.row_index = i
  value.column_index = i
  value.value = random.randint(10,15)
for i in range(1, 5000):
  value = matrix_a_proto.values.add()
  value.row_index = i
  value.column_index = i-1
  value.value = random.randint(2,4)
for i in range(0, 4999):
  value = matrix_a_proto.values.add()
  value.row_index = i
  value.column_index = i+1
  value.value = random.randint(-4,4)
  
matrix_a = sparse_matrix.SparseMatrix(matrix_a_proto)

# Create vector with 5000 entries
vector_a_list = []
for i in range(5000):
  vector_a_list.append(random.randint(10,20))

vector_b = vector.Vector(name = "a", number_list = vector_a_list)

large_matrix_sor = effect_relaxation_rate(matrix_a, vector_b)

table2 = pandas.DataFrame({'relaxation_rate':index_list,
                           'large_matrix': large_matrix_sor}).set_index(
                           'relaxation_rate')
                           
pyplot.plot(table2[:1.2])
pyplot.ylabel('Number of Iterations Run')
pyplot.xlabel('Relaxation Rate')
pyplot.legend(["large_matrix"], loc=9,ncol=4)
pyplot.show()