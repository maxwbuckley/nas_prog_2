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
    self.stopping_reason = sor_pb2.SorReturnValue.UNKNOWN
    self.x = [0] * self.b.length
    self.sparse_sor()

  def __repr__(self):
    print_template = """
        Input Matrix A:\n%(MATRIX_A)s
        Input Vector b: %(VECTOR_B)s
        Stopping Reason: %(STOP_REASON)s
        Computed vector x: %(OUTPUT_X)s"""
    return print_template % {
        "MATRIX_A": self.A, "VECTOR_B": self.b, "STOP_REASON":
        sor_pb2.SorReturnValue.StoppingReason.Name(self.stopping_reason),
                             "OUTPUT_X": self.x}

  def sparse_sor(self):
    """Compute the sparse sor solution for Ax = b.
    Returns:
      A list of numeric values and a termination reason.
    """
    k = 0
    self.x_old = None
    while not self.is_converged() and k <= self.maxits:
      self.x_old = self.x[:]
      for i in range(self.b.length):
        sum = 0
        for j in range(self.A.rowStart[i], self.A.rowStart[i + 1]):
          sum = sum + self.A.vals[j] * self.x[self.A.cols[j]]
          if self.A.cols[j] == i:
            d = self.A.vals[j]
        self.x[i] = (
            self.x[i] + self.relaxation_rate * (self.b.values[i] - sum) / d)
      k += 1
    if k >= self.maxits:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.MAX_ITERATIONS_REACHED)


  def is_converged(self):
    """Performs a series of convergence checks.

    Updates the self.stopping_reason variable if necessary

    Returns:
      boolean whether we should stop.
    """
    if self.x_old is None:
      self.total_old = float("inf")
      return False
    x_total = 0
    for i in range(len(self.x)):
      x_total += abs(self.x[i] - self.x_old[i])
    if x_total > self.total_old:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.X_SEQUENCE_DIVERGENCE)
      return True
    estimate = self.A.multiply_by_vector(vector.Vector(number_list=self.x))
    residual_total = 0
    for i in range(len(estimate)):
      residual_total += abs(self.b.values[i] - estimate[i])
    # Threshold is defined as the sum of the passed tolerance and a multiple
    # of machine epsilon.
    threshold = (
        self.tolerance + 4.0 * self.machine_epsilon * abs(x_total))
    if x_total <= threshold:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.X_SEQUENCE_CONVERGENCE)
      return True
    if residual_total <= threshold:
      self.stopping_reason = (
          sor_pb2.SorReturnValue.RESIDUAL_CONVERGENCE)
      return True
    return False
