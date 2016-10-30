"""Class and methods pertaining to Sparse Matrices."""


class NonConformableException(Exception):
  """Exception for when tries to multiply non conformable matrices."""
  pass


class SparseMatrix(object):
  def __init__(self, sparse_matrix_proto):
    # Lots to do here.
    pass
 
  def multiply(self, vector):
    """Multiply this matrix by the target vector
  
      Args:
        vector:
      Returns:
        a vector.
      Raises NonConformableException if the matrix and vector are non
          conformable.
    """
    pass

  def is_conformable(self, matrix):
    """Returns a boolean if the two matrices are conformable.
    
    Returns:
      boolean.
    """
    pass
   
