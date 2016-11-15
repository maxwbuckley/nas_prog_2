#! /usr/bin/python3
"""This script is to experiment with different parameters on different parts
   of our program."""
   
import sparse_matrix
import vector
import sparse_sor
import pandas

# Createa number of matrices and vectors to experiment with    
matrix_a = sparse_matrix.SparseMatrix(dense_matrix=
      [[7, 1, 0, 3, 0],
       [0, -7, 1, 0, 0],
       [1, 0, 8, 2, 0],
       [1, 0, 0, 7, 2],
       [-1, 0, -1, 0, 9]])
  
vector_b = vector.Vector(name = "b", number_list = [1, 1, 2, 2, 3])

matrix_b = sparse_matrix.SparseMatrix(dense_matrix=
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
  
vector_d = vector.Vector(name = "d",
                         number_list = [3, 4, 3, 2, 3, 1, 5, 3, 1, 2])
                         
matrix_c = sparse_matrix.SparseMatrix(dense_matrix=
      [[15, 1, 0, 3, 0, 4, 0],
       [0, -14, 0, 0, 0, 3, 0],
       [1, 0, 21, 0, 1, 0, 3],
       [1, 0, 0, 20, 3, 0, 5],
       [0, 0, -1, 2, -19, 0, 5],
       [0, 1, 0, 3, 0, -14, 4],
       [0, 0, 1, 0, 0, 3, 23]])
  
vector_f = vector.Vector(name = "f",
                         number_list = [3, 4, 3, 5, 3, 1, 2])

# Creat list of relaxation rates to act as indices                         
index_list = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
                         
def experiment_EffectOfDifferentRelaxationRate(matrix,
                                               vector, relaxation_rate):
  """Calculate resudual sum for a matrix with different relaxation rates.
  
  Args:
    matrix: A sparse_matrix.Matrix. This needs to be diagonally dominant.
    vector: A vector.Vector
    
  Returns: List of sum of residuals for different relaxation rates.
  """
  i = 1.0
  results = []
  while(i < 2.1):
    sparse_sor_solver = sparse_sor.SparseSorSolver(
        matrix, vector, relaxation_rate, 10**-20, i)
    results.append(sparse_sor.SparseSorSolver.compute_absolute_residual_sum(
            sparse_sor_solver))  
    i += 0.1
  return(results)

experiment_a = experiment_EffectOfDifferentRelaxationRate(matrix_a, 
                                                          vector_b, 10)
experiment_b = experiment_EffectOfDifferentRelaxationRate(matrix_b, 
                                                          vector_d, 10)
experiment_c = experiment_EffectOfDifferentRelaxationRate(matrix_c, 
                                                          vector_f, 10)
experiment_d = experiment_EffectOfDifferentRelaxationRate(matrix_a, 
                                                          vector_b, 5)
experiment_e = experiment_EffectOfDifferentRelaxationRate(matrix_b, 
                                                          vector_d, 5)
experiment_f = experiment_EffectOfDifferentRelaxationRate(matrix_c, 
                                                          vector_f, 5)
experiment_g = experiment_EffectOfDifferentRelaxationRate(matrix_a, 
                                                          vector_b, 20)
experiment_h = experiment_EffectOfDifferentRelaxationRate(matrix_b, 
                                                          vector_d, 20)
experiment_i = experiment_EffectOfDifferentRelaxationRate(matrix_c, 
                                                          vector_f, 20)

table1 = pandas.DataFrame({'relaxation_rate':index_list,
                           'matrix_a':experiment_a,'matrix_b':experiment_b,
                           'matrix_c':experiment_c})
table2 = pandas.DataFrame({'relaxation_rate':index_list,
                           'matrix_a':experiment_d,'matrix_b':experiment_e,
                           'matrix_c':experiment_f})
table3 = pandas.DataFrame({'relaxation_rate':index_list,
                           'matrix_a':experiment_g,'matrix_b':experiment_h,
                           'matrix_c':experiment_i})

table1_with_index = table1.set_index('relaxation_rate')
table2_with_index = table2.set_index('relaxation_rate')
table3_with_index = table3.set_index('relaxation_rate')

# Print results to be added to assignment doc
print(table1_with_index)
print(table2_with_index)
print(table3_with_index)


""" Black-Scholes with Google stock options """

""" Option 1 """

r = 0.54
sigma = 35
stock_price_max = 835.74
h = 83574
timesteps = 7
strike_price = 730

k = 1/365

def start_prices(strike_price, stock_prices_time_0):
  return [max(strike_price - stock_price, 0) for
          stock_price in stock_prices_time_0]


def generate_black_scholes_matrix(N, k, sigma, r):
  grid =[[0 for _ in range(N)] for _ in range(N)]
  for i in range(N):
    n = i + 1
    if i > 0:
      # Append previous row
      grid[i][i-1] = -((n * k) / 2) * (n * sigma ** 2 - r)
    # Append current row
    grid[i][i] = 1 + (k * r) + (k * (sigma ** 2) * (n ** 2))
    if i < N - 1:
      # Append final element
      grid[i][i + 1] =  -((n * k) / 2) * (n * (sigma ** 2) + r)
  return grid


def generate_adjustment_term(strike_price, k, sigma, r):
  return ((k / 2) * (sigma ** 2 - r) * strike_price)

def generate_stock_price_array(stock_price_max, h):
  return [stock_price_max * (price / h) for price in range(
          h + 1)]

def generate_option_price_grid(
    timesteps, strike_price, h, k, sigma, r, stock_price_array):
  option_price_grid =[[None for _ in range(h + 1)] for _ in range(
      timesteps + 1)]
  # row is across prices columns are over time
  option_price_grid[0] = start_prices(strike_price, stock_price_array)
  # A matrix will have N-2 * N-2 elements. Of which only 3 * N-2 are populated
  A = sparse_matrix.SparseMatrix(dense_matrix=generate_black_scholes_matrix(
      h - 1, k, sigma, r))

  adjustment = generate_adjustment_term(strike_price, k, sigma, r)
  time_step = 1
  while time_step < (timesteps + 1):
    # Need to create a new list here to avoid Python list mutability.
    f_vector = option_price_grid[time_step - 1][:]
    # Need to adjust 1st element by adding adjustment term.
    f_vector[1] += adjustment
    f = vector.Vector(number_list=f_vector[1:-1])
    sparse_sor_solver = sparse_sor.SparseSorSolver(A, f, 100, .0001, 1.0)
    option_price_grid[time_step] = (
        [strike_price] + sparse_sor_solver.get_solution().values + [0])
    time_step += 1
  return option_price_grid

def run_black_scholes(
    timesteps, strike_price, h ,k, sigma, r, stock_price_max):
  if (k / h ** 2) >= 1 / 2:
    raise Exception("k/h**2 needs to be less than 1/2 for stability")
  print("Price intervals: %s\nTime_interval: %s days"
        % (h + 1, timesteps))
  stock_price_array = generate_stock_price_array(stock_price_max, h)
  option_price_grid = generate_option_price_grid(
      timesteps, strike_price, h, k, sigma, r, stock_price_array)
  return {stock_price: option_price for stock_price, option_price in
          zip(stock_price_array, option_price_grid[-1])}



if __name__ == "__main__":
  values = run_black_scholes(
      timesteps, strike_price, h, k, sigma, r, stock_price_max)
  for key, value in sorted(values.items()):
    print("Stock price: %s, Option price: %s" % (key, value))

