"""Docstring"""
import sparse_matrix
import vector

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
    self.A = matrix
    self.b = vector
    self.maxits = maxits
    self.tolerance = e
    self.relaxation_rate = w

    # Fill out
    self.stopping_reason = None
    self.x = [0] * self.b.length
    self.sparse_sor()
 
  def __repr__(self):
    print_template = """
        Input Matrix A:\n%(MATRIX_A)s
        Output Vector b: %(VECTOR_B)s
        Stopping Reason: %(STOP_REASON)s
        Computed vector x: %(OUTPUT_X)s"""
    return print_template % {"MATRIX_A": self.A, "VECTOR_B": self.b,
                             "STOP_REASON": self.stopping_reason,
                             "OUTPUT_X": self.x}
 
  def sparse_sor(self):
    """Compute the sparse sor solution for Ax = b.
    Returns:
      A list of numeric values and a termination reason.
    """
    k = 0
    while not self.converged() and k <= self.maxits:
      for i in range(self.b.length):
        sum = 0
        for j in range(self.A.rowStart[i], self.A.rowStart[i + 1]):
          sum = sum + self.A.vals[j] * self.x[self.A.cols[j]]
          if self.A.cols[j] == i:
            d = self.A.vals[j]
        self.x[i] = self.x[i] + self.relaxation_rate * (self.b.values[i] - sum) / d
      k += 1
    # Need to set stopping rule.


  def converged(self):
    # Use the tolerance here.
    return False
