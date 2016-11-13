#! /usr/bin/python3

import math
import sparse_matrix
import vector
import sparse_sor


r = 0.02/365 # Per timestep
sigma = .3 # Per timestep
stock_price_max = 2.0 # dollars, can be a float.
h = 200 # price sub intervals. Int
timesteps = 30 # days Int
k = 5 # time sub_intervals (trading hours)? Int
strike_price = 1.00 # Price at which we can sell our asset at time 0

def start_price(strike_price, stock_price_time_0):
  """This calculates the price of the option at time 0.

  Args:
    strike_price: The strike price of the option in question.
    stock_price_time_0: the stock price at time 0.
  Returns:
    A float greater than or equal to 0.
  """
  return max(strike_price - stock_price_time_0, 0)

def generate_black_scholes_matrix(
  strike_price, N, subintervals, sigma_base, r_base):
  """Generates the black scholes matrix and adjustment

  Args:
    strike_price: The strike price of the option in question.
    N: The desired dimension of the matrix. we want to work from 0 to N-1.
    subintervals: k the number of intervals into which each timestep is broken.
    sigma_base: The base standard_deviation
    r_base: The base risk free rate.

  Returns:
    A tuple of a dense matrix (list of lists) and a float adjustment figure to
        be added to f_1, m+1.
  """
  # Discuss with guys.
  r = r_base / subintervals
  sigma = sigma_base  / subintervals
  # End discussion.
  k = subintervals
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
  # This is only here due to adjustments to r and sigma above.
  adjustment_term = (k / 2) * (sigma ** 2 - r) * strike_price
  return (grid, adjustment_term)


if __name__ == "__main__":
  if (k / h ** 2) >= 1 / 2:
    raise Exception("k/h**2 needs to be less than 1/2 for stability")


  price_intervals = h + 1
  time_intervals = (timesteps * k) + 1

  print("Price intervals: %s\nTime_intervals: %s" % (
      price_intervals, time_intervals))
  stock_price_array = [stock_price_max * (price / h) for price in range(
      price_intervals)]
  option_price_grid =[[None for _ in range(price_intervals)] for _ in range(
      time_intervals)]
  # row is across prices columns are over time
  # Need to set inital values
  # Set first row time=0.
  for i in range(len(option_price_grid[0])):
    option_price_grid[0][i] = start_price(strike_price, stock_price_array[i])
  # A matrix will have N-2 * N-2 elements. Of which only 3 * N-2 are populated
  (A_dense, adjustment) = generate_black_scholes_matrix(
      strike_price, price_intervals -2, k, sigma, r)
  A = sparse_matrix.SparseMatrix(dense_matrix=A_dense)

  time_step = 1
  while time_step < time_intervals:
    f_vector = option_price_grid[time_step - 1][:]
    # Need to adjust 1st element by adding adjustment term.
    f_vector[1] += adjustment
    f = vector.Vector(number_list=f_vector[1:-1])
    sparse_sor_solver = sparse_sor.SparseSorSolver(A, f, 100, .0001, 1.0)
    option_price_grid[time_step] = (
        [strike_price] + sparse_sor_solver.get_solution().values + [0])
    time_step += 1

  print(*zip(stock_price_array, option_price_grid[-1]))
