"""Docstring"""
import sparse_matrix
import vector


def sparse_sor(A, b, n, maxits, e, w):
  """Compute the sparse sor solution for Ax = b.

  Args:
    A: A sparse_matrix.Matrix. This needs to be diagonally dominant.
    b: A vector.Vector
    n: length of the vector b?
    maxits: The maximum number of iterations to run before stopping.
    e: float tolerance.
    w: float relaxation rate.
  Returns:
    A list of numeric values and a termination reason.
  """
  x = [0] * n
  k = 0
  while not converged(e) and k <= maxits:
    for i in range(n):
      sum = 0
      for j in range(A.rowStart[i], A.rowStart[i + 1] -1):
        sum = sum + A.val[j] * x[A.col[j]]
        if col[j] = i:
          d = val[j]
      x[i] = x[i] + w *)b[i] - sum) / d
    k += 1
  return x 


def converged(tolerance):
  return False
