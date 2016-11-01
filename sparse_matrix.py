"""Class and methods pertaining to Sparse Matrices."""
import validation
import vector

class NonConformableException(Exception):
  """Exception for when one tries to multiply non conformable matrices."""
  pass


class SparseMatrix(object):
  def __init__(self, sparse_matrix_proto):
    """Initialize Sparse Matrix.

    Args:
      sparse_matrix_proto: A sor_pb2.SparseMatrix proto.
    """
    validation.ValidateSparseMatrixProto(sparse_matrix_proto)
    self.columns = sparse_matrix_proto.column_count
    self.rows = sparse_matrix_proto.row_count
    self.rowStart, self.cols, self.vals = self._get_csr_structure(
      sparse_matrix_proto.values)

  def _get_csr_structure(self, sparse_value_protos):
    temp_list = []
    for value in sparse_value_protos:
      temp_list.append((value.row_index, value.column_index, value.value))
    sorted_list = sorted(temp_list, key=lambda element: (element[0], element[1]))
    # popping left is O(n). Better to replace with a queue.
    row, col, val = sorted_list.pop(0)
    rowStart = [row]
    cols = [col]
    vals = [val]
    for row in sorted_list:
      if row[0] > rowStart[-1]:
        rowStart.append(row[0])
      cols.append(row[1])
      vals.append(row[2])
    # Add sentinel value.
    rowStart.append(self.rows)
    return rowStart, cols, vals

  def __repr__(self):
    return '\n'.join([str(row) for row in self.to_dense_matrix()])

  def to_dense_matrix(self):
    """Returns a dense matrix corresponding to this sparse matrix."""
    dense_mat = [[0 for column in range (self.columns)]
                 for row in range(self.rows)]
    for i in range(self.rows):
      for j in range(self.rowStart[i], self.rowStart[i + 1]):
        dense_mat[i][self.cols[j]] = self.vals[j]
    return dense_mat

    

  def multiply(self, vector):
    """Multiply this matrix by the target vector
  
      Args:
        vector:
      Returns:
        a vector.
      Raises NonConformableException if the matrix and vector are non
          conformable.
    """
    if not isinstance(vector, vector.Vector):
      raise Exception("Can only multiply by a vector")
    # New empty 0 vector
    new_vec = [0] * vector.length
    

  def is_conformable(self, vector):
    """Returns a boolean if the two matrices are conformable.
    
    Args:
      vector: a vector.Vector object.    

    Returns:
      boolean if this Matrix and that vector are conformable.
    Raises:
      NonConformableException if the dimensions don't match.
    """
    if this.columns == vector.length:
      return True
    raise NonConformableException
   
