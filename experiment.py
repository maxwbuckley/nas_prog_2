#! /usr/bin/python3 
"""This script is to experiment with different parameters on different parts
   of our program."""

import sparse_matrix
import vector
import sparse_sor
import pandas
from proto_genfiles.protos import sor_pb2
import random
from matplotlib import pyplot


# Create a number of matrices and vectors to experiment with

positive_definite_symmetric = sparse_matrix.SparseMatrix(dense_matrix=
  [[2, -1, 0],
  [-1, 2, -1],
  [0, -1, 2]])

vector_b_1 = vector.Vector(name = "b", number_list = [1, 1, 1])

diag_dominant_a = sparse_matrix.SparseMatrix(dense_matrix=
      [[7, 1, 0, 3, 0],
       [0, -7, 1, 0, 0],
       [1, 0, 8, 2, 0],
       [1, 0, 0, 7, 2],
       [-1, 0, -1, 0, 9]])

vector_b_2 = vector.Vector(name = "b", number_list = [1, 1, 2, 2, 3])

diag_dominant_b = sparse_matrix.SparseMatrix(dense_matrix=
      [[15, 1, 0, 0, 0, 4, 0, 0, 1, 0],
       [0, -14, 1, 0, 0, 3, 0, 0, 1, 2],
       [1, 0, 21, 0, 1, 0, 3, 2, 0, 0],
       [1, 0, 0, 20, 3, 0, 5, 2, 0, 0],
       [-1, 0, -1, 2, -19, 0, 0, 2, 0, 0],
       [0, 1, 0, 3, 0, -14, 4, 0, 1, 0],
       [0, -3, 1, 0, 0, 3, 23, 0, 1, 0],
       [1, 0, 0, 0, 1, 0, 3, 20, 0, 0],
       [1, 0, 0, 2, 3, 0, 0, 2, 19, 0],
       [-1, 0, 0, 0, -9, 0, 5, 2, 0, 29]])

vector_b_3 = vector.Vector(name = "d",
                         number_list = [3, 4, 3, 2, 3, 1, 5, 3, 1, 2])

diag_dominant_c = sparse_matrix.SparseMatrix(dense_matrix=
      [[15, 1, 0, 3, 0, 4, 0],
       [0, -14, 0, 0, 0, 3, 0],
       [1, 0, 21, 0, 1, 0, 3],
       [1, 0, 0, 20, 3, 0, 5],
       [0, 0, -1, 2, -19, 0, 5],
       [0, 1, 0, 3, 0, -14, 4],
       [0, 0, 1, 0, 0, 3, 23]])

vector_b_4 = vector.Vector(name = "f",
                         number_list = [3, 4, 3, 5, 3, 1, 2])

# Create list of relaxation rates to act as indices
index_list = [ x / 100 for x in range(10,201)]

print("-----------------------------------------")
print("Show effect of different relaxation rates")
print("-----------------------------------------")

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
  while(i < 2.01):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix, vector, maxits, 2**-20, i)
    results.append(sparse_sor_solver.iteration)
    i += 0.01
  return(results)

positive_def = effect_relaxation_rate(positive_definite_symmetric, vector_b_1)
diag_a = effect_relaxation_rate(diag_dominant_a, vector_b_2)
diag_b = effect_relaxation_rate(diag_dominant_b, vector_b_3)
diag_c = effect_relaxation_rate(diag_dominant_c, vector_b_4)

table = pandas.DataFrame({'relaxation_rate':index_list,
                           'positive_def': positive_def, 'diag_a': diag_a,
                           'diag_b':diag_b, 'diag_c':diag_c}).set_index(
                           'relaxation_rate')
                           
pyplot.plot(table)
pyplot.ylabel('Number of Iterations Run')
pyplot.xlabel('Relaxation Rate')
pyplot.legend(["diag_c","diag_a","diag_b","positive_def"], loc=9,ncol=4)
pyplot.show()

# Print results to be added to assignment doc

print("------------------------------------------------------------------")
print("Show effect of setting relaxation rate set to out of bounds number")
print("------------------------------------------------------------------")

# Experiment to see effect of setting relaxation rate to out of bounds number
sparse_sor_solver_a = sparse_sor.SparseSorSolver(positive_definite_symmetric,
                                                 vector_b_1, 50, 10**-10, 20)

sparse_sor_solver_b = sparse_sor.SparseSorSolver(diag_dominant_a,
                                                 vector_b_2, 50, 10**-10, 20)

sparse_sor_solver_c = sparse_sor.SparseSorSolver(diag_dominant_b, 
                                                 vector_b_3, 50, 10**-10, 20)
        
sparse_sor_solver_d = sparse_sor.SparseSorSolver(diag_dominant_c,
                                                 vector_b_4, 50, 10**-10, 20)

print(sparse_sor_solver_a)
print(sparse_sor_solver_b)
print(sparse_sor_solver_c)
print(sparse_sor_solver_d)

""" Black-Scholes with Google stock options """

""" Option 1 """

r = 0.54
sigma = 35
stock_price_max = 835.74
h = 83574
timesteps = 7 # Days
m = 28 # TIme sub intervals
strike_price = 730

k = 1/365

# Experiment to see effect of poorly-conditioned matrix on sparse_sor

print("------------------------------------------------------------")
print("Show effect of poorly-conditioned and ill-conditioned matrix")
print("------------------------------------------------------------")

matrix_poor_conditioned = sparse_matrix.SparseMatrix(dense_matrix=
      [[1.01, 1],
       [1, 1.01]])
       
matrix_ill_conditioned = sparse_matrix.SparseMatrix(dense_matrix=
      [[1, 0.99],
       [0.99, 0.98]])
       
vector_poor_conditioned = vector.Vector(name = "b", number_list = [2, 2])

vector_ill_conditioned = vector.Vector(name = "b", number_list = [2, 2])

poor_condition = effect_relaxation_rate(matrix_poor_conditioned,
                                        vector_poor_conditioned, maxits=500)
                       
ill_condition = effect_relaxation_rate(matrix_ill_conditioned,
                                       vector_ill_conditioned, maxits=500)

table1 = pandas.DataFrame({'relaxation_rate':index_list,
                           'poor_condition': poor_condition,
                           'ill_condition': ill_condition}).set_index(
                           'relaxation_rate')
                           
pyplot.plot(table1)
pyplot.ylabel('Number of Iterations Run')
pyplot.xlabel('Relaxation Rate')
pyplot.legend(["ill_condition","poor_condition"], loc=9,ncol=4)
pyplot.show()

# Experiment to see effect of different levels of tolerance

print("--------------------------------------------")
print("Show effect of different levels of tolerance")
print("--------------------------------------------")

def experiment_EffectOfDifferentTolerance(matrix, vector):
  """Calculate residual sum for a matrix with different relaxation rates.
  
  Args:
    matrix: A sparse_matrix.Matrix. This needs to be diagonally dominant.
    vector: A vector.Vector
    
  Returns: List of sum of residuals for different relaxation rates.
  """
  i = -1
  while(i > -22):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix, vector, 50, 10**i, 1.0)
    print(sparse_sor_solver)
    i -= 4
   
experiment_EffectOfDifferentTolerance(positive_definite_symmetric, vector_b_1)
experiment_EffectOfDifferentTolerance(diag_dominant_a, vector_b_2)
experiment_EffectOfDifferentTolerance(diag_dominant_b, vector_b_3)
experiment_EffectOfDifferentTolerance(diag_dominant_c, vector_b_4)

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
                           
pyplot.plot(table2)
pyplot.ylabel('Number of Iterations Run')
pyplot.xlabel('Relaxation Rate')
pyplot.legend(["large_matrix"], loc=9,ncol=4)
pyplot.show()