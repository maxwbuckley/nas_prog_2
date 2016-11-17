#! /usr/bin/python3
"""This script is for running the black sholes algorithm for option pricing."""

import math
import sparse_matrix
import vector
import sparse_sor

# These values can be adjusted as required.

r = 0.02 # Risk free rate of return per day.
sigma = .2 # Daily standard deviation.
stock_price_max = 2.0 # dollars, Float.
h = 200 # price sub intervals, Int.
time_to_exercise = 60 # days to excise Int.
timesteps_total = 90 # m the number of time_intervals to split t into Int.
strike_price = 1.0 # Price at which we can sell our asset at time 0.

# scalar for converting rates to relevant time period of days.
k = (time_to_exercise/timesteps_total)/365

def start_prices(strike_price, stock_prices_time_0):
  """This calculates the list of start prices of the option at time 0.

  Args:
    strike_price: The strike price of the option in question.
    stock_price_time_0: List of all the possible stock prices at time 0.
  Returns:
    A list of the prices of the option.
  """
  return [max(strike_price - stock_price, 0) for
          stock_price in stock_prices_time_0]


def generate_black_scholes_matrix(N, k, sigma, r):
  """Generates the black scholes matrix and adjustment

  Args:
    N: The desired dimension of the matrix. we want to work from 0 to N-1.
    k: The number of intervals into which each timestep is broken.
    sigma: The standard deviation
    r: The risk free rate.

  Returns:
    A dense matrix (list of lists).
  """
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
  """Generate the adjustment term for f_(1,m+1).

  Args:
    strike_price: The strike price of the option in question.
    k: k the number of intervals into which each timestep is broken.
    sigma: The standard deviation
    r: The risk free rate.

  Returns:
    A float adjustment figure to be added to f_(1, m+1).
  """
  return ((k / 2) * (sigma ** 2 - r) * strike_price)


def generate_stock_price_array(stock_price_max, h):
  """Generates the list of potentital stock prices.

  Args:
    stock_price_max: At stock price at which the option is worth 0.
    h: The number of intervals we want to split 0 to the max price into.
  Returns:
    A list of the stock prices in order from lowest to highest.
  """
  return [stock_price_max * (price / h) for price in range(
          h + 1)]


def generate_option_price_grid(
    timesteps, strike_price, h, k, sigma, r, stock_price_array):
  """Generate the matrix of option prices for each price, timestep pair.

  Args:
    timesteps: The integer number of timesteps to run for.
    strike_price: The strike price of the option in question.
    h: h the number of intervals into which the price is broken.
    k: k the number of intervals into which each timestep is broken.
    sigma: The standard deviation
    r: The risk free rate.

  Returns:
    A list of lists matrix. The  rows are for different stock prices and the
        columns are the different timesteps.
  """
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
    time_to_exercise, timesteps, strike_price, h ,k, sigma, r, stock_price_max):
  """Runs the black scholes program.

  Args:
    time_to_exercise: The integer number of days to run for.
    timesteps: The integer number of timesteps to break down to.
    strike_price: The strike price of the option in question.
    h: h the number of intervals into which the price is broken.
    k: k the number of intervals into which each timestep is broken.
    sigma: The standard deviation
    r: The risk free rate.

  Returns:
    A dict mapping the stock price at time timestep to the option price.
  Raises:
    Exception if the passed k and h values are unstable.
  """
  if (k / h ** 2) >= 1 / 2:
    raise Exception("k/h**2 needs to be less than 1/2 for stability")
  print("Price intervals: %s\nTime_intervals: %s days"
        % (h + 1, time_to_exercise))
  stock_price_array = generate_stock_price_array(stock_price_max, h)
  option_price_grid = generate_option_price_grid(
      timesteps, strike_price, h, k, sigma, r, stock_price_array)
  return {stock_price: option_price for stock_price, option_price in
          zip(stock_price_array, option_price_grid[-1])}



if __name__ == "__main__":
  values = run_black_scholes(
      time_to_exercise,
      timesteps_total, strike_price, h, k, sigma, r, stock_price_max)
  for key, value in sorted(values.items()):
    print("Stock price: %s, Option price: %s" % (key, value))
