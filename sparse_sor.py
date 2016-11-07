"""Docstring"""
import sparse_matrix
import vector
from proto_genfiles.protos import sor_pb2


class SorSolverInputException(Exception):
  """An exception for when the inputs are not compatible."""

class SparseSorSolver(object):
  def __init__(self, matrix, vector, maxits=10, e=.01, w=1.0):
    """Docstring

    Args:
      A: A sparse_matrix.Matrix. This needs to be diagonally dominant.
      b: A vector.Vector
      maxits: The maximum number of iterations to run before stopping.
      e: float tolerance.
      w: float relaxation rate.
    """
    # Need to perform checks here.
    if not matrix.is_strictly_row_diagonally_dominant():
      # This is also checking for zero on diagonal.
      raise SorSolverInputException("Input matrix is not strictly diagonally "
                                    "dominant.")
    self.A = matrix
    self.b = vector
    self.maxits = maxits
    self.tolerance = e
    self.relaxation_rate = w

    self.machine_epsilon = 2 ** -52
    self.sor_return_proto = sor_pb2.SorReturnValue()
    # Fill out
    self.iteration = 0
    self.stopping_reason = sor_pb2.SorReturnValue.UNKNOWN
    self.x = [0] * self.b.length
    self.x_old = None
    self.total_old = float("inf")
    self.sparse_sor()

  def __repr__(self):
    print_template = """
        Input Matrix A:\n%(MATRIX_A)s
        Input Vector b: %(VECTOR_B)s
        Stopping reason: %(STOP_REASON)s
        Stopping iteration: %(ITERATION)s
        Computed vector x: %(OUTPUT_X)s
        Sum of absolute residual: %(RESIDUAL)s
        """

    return print_template % {
        "MATRIX_A": self.A,
        "VECTOR_B": self.b,
        "STOP_REASON":
            sor_pb2.SorReturnValue.StoppingReason.Name(self.stopping_reason),
        "ITERATION": self.iteration,
        "OUTPUT_X": self.x,
        "RESIDUAL": self.compute_absolute_residual_sum()}

  def sparse_sor(self):
    """Compute the sparse sor solution for Ax = b.
    Returns:
      A list of numeric values and a termination reason.
    """
    while not self.is_converged() and self.iteration < self.maxits:
      self.x_old = self.x[:]
      for i in range(self.b.length):
        sum = 0
        for j in range(self.A.rowStart[i], self.A.rowStart[i + 1]):
          sum = sum + self.A.vals[j] * self.x[self.A.cols[j]]
          if self.A.cols[j] == i:
            d = self.A.vals[j]
        self.x[i] = (
            self.x[i] + self.relaxation_rate * (self.b.values[i] - sum) / d)
      self.iteration += 1
    if self.iteration >= self.maxits:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)

  def compute_absolute_residual_sum(self):
    """Computes the sum of the absolute deviations from Ax from b"""
    estimate = self.A.multiply_by_vector(vector.Vector(number_list=self.x))
    residual_total = 0
    for i in range(len(estimate)):
      residual_total += abs(self.b.values[i] - estimate[i])
    return residual_total

  def compute_absolute_x_sequence_difference_sum(self):
    """Calculate the absolute difference between the current x and last x."""
    x_diff_sum = 0
    for i in range(len(self.x)):
      x_diff_sum += abs(self.x[i] - self.x_old[i])
    return x_diff_sum

  def calculate_stopping_threshold(self, value):
    """Calculate the stopping threshold for a given value."""
    return self.tolerance + 4.0 * self.machine_epsilon * abs(value)

  def is_converged(self):
    """Performs a series of convergence checks.

    Updates the self.stopping_reason variable if necessary

    Returns:
      boolean whether we should stop.
    """
    if self.x_old is None:
      return False
    x_total = self.compute_absolute_x_sequence_difference_sum()
    if x_total > self.total_old:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.X_SEQUENCE_DIVERGENCE)
      return True
    x_threshold = self.calculate_stopping_threshold(x_total)
    if x_total <= x_threshold:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.X_SEQUENCE_CONVERGENCE)
      return True
    residual_threshold = self.calculate_stopping_threshold(1)
    if self.compute_absolute_residual_sum() <= residual_threshold:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.RESIDUAL_CONVERGENCE)
      return True
    return False
