"""Docstring"""
import sparse_matrix
import vector
from proto_genfiles.protos import sor_pb2


class SorSolverInputException(Exception):
  """An exception for when the inputs are not compatible."""

class SparseSorSolver(object):
  def __init__(self, matrix, vector, maxits=10, e=.01, w=1.0):
    """Initialize Sparse SOR Solver

    Args:
      matrix: A sparse_matrix.Matrix. This needs to be diagonally dominant.
      vector: A vector.Vector
      maxits: The maximum number of iterations to run before stopping.
      e: float tolerance.
      w: float relaxation rate.
    """
    # Need to perform checks here.
    if not matrix.is_strictly_row_diagonally_dominant():
      # This is also checking for zero on diagonal.
      raise SorSolverInputException("Input matrix is not strictly diagonally "
                                    "dominant.")
    if not matrix.rows == vector.length:
      print("Matrix rows: %s" % matrix.rows)
      print("Vector length: %s" % vector.length)
      raise Exception("Lengths are not conformable Ax = b hence rows in A "
                      "must equal rows in b")
    self.A = matrix
    self.b = vector
    self.maxits = maxits
    self.tolerance = e
    self.relaxation_rate = w

    self.machine_epsilon = 2 ** -52

    # Fill out
    self.iteration = 0
    self.stopping_reason = sor_pb2.SorReturnValue.UNKNOWN
    self.x = [0] * self.b.length
    self.x_old = None
    self.total_old = float("inf")
    self.sparse_sor()

  def __repr__(self):
    """Change print format"""
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
    # Update old X total.
    self.total_old = x_total
    return False

  def get_solution(self):
    """Returns the solution vector x.

    Returns:
      A vector.Vector of the solution x.
    """
    return vector.Vector(number_list = self.x)

  def to_proto(self):
    """Converts solution to proto for storage and transmission."""
    return sor_pb2.SorReturnValue(
        result_name="x", stopping_reason=self.stopping_reason,
        vector=self.get_solution().to_proto(),
        stopping_iteration=self.iteration)
