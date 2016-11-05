"""Class and methods pertaining to Sparse Matrices."""
import validation
import vector

class NonConformableException(Exception):
  """Exception for when one tries to multiply non conformable matrices."""
  pass


class SparseMatrix(object):
  def __init__(self, sparse_matrix_proto=None, dense_matrix=None):
    """Initialize Sparse Matrix.

    Args:
      sparse_matrix_proto: A sor_pb2.SparseMatrix proto.
      dense_matrix: A list of lists with only numerical entries.
    """
    if not (sparse_matrix_proto or dense_matrix):
      raise Exception("Need to pass a proto or matrix to constructor")
    if sparse_matrix_proto and dense_matrix:
      raise Exception("Both should not be submitted")
    if sparse_matrix_proto:
      self.from_proto(sparse_matrix_proto)
    else:
      self.from_dense_matrix(dense_matrix)
  
  def from_dense_matrix(self, dense_matrix):
    """Construct from dense matrix.

    Args:
      dense_matrix: A list of lists with only numerical entries.
    """
    validation.ValidateNumberList(dense_matrix)
    self.columns = len(dense_matrix[0])
    self.rows = len(dense_matrix[0])
    self.rowStart, self.cols, self.vals = self._get_csr_structure(
      dense_matrix=dense_matrix)

  def from_proto(self, sparse_matrix_proto):
    """Construct from sparse matrix proto.

    Args:
      sparse_matrix_proto: A sor_pb2.SparseMatrix proto.
    """
    validation.ValidateSparseMatrixProto(sparse_matrix_proto)
    self.columns = sparse_matrix_proto.column_count
    self.rows = sparse_matrix_proto.row_count
    self.rowStart, self.cols, self.vals = self._get_csr_structure(
      sparse_matrix_proto.values)


  def _convert_dense_matrix_to_tuple_list(self, dense_matrix):
    """Convert a dense matrix into a list of its non 0 valued tuples.
    Args:
      dense_matrix: A list of lists with only numerical entries.
    Returns:
      A list of tuples of the form row index, col_indes, value.
    """
    tuple_list = []
    for i in range(len(dense_matrix)):
      for j in range(len(dense_matrix[0])):
        if dense_matrix[i][j] != 0:
          tuple_list.append((i, j, dense_matrix[i][j]))
    return tuple_list

  def _convert_proto_to_tuple_list(self, sparse_value_proto):
    tuple_list = []
    for value in sparse_value_proto:
      tuple_list.append((value.row_index, value.column_index, value.value))
    return tuple_list

  def _get_csr_structure(self, sparse_value_proto=None, dense_matrix=None):
    # Need some checking
    if sparse_value_proto is not None:
      temp_list = self._convert_proto_to_tuple_list(sparse_value_proto)
    elif dense_matrix is not None:
      temp_list = self._convert_dense_matrix_to_tuple_list(dense_matrix)
    sorted_list = sorted(temp_list, key=lambda element: (element[0], element[1]))
    print(sorted_list)
    # popping left is O(n). Better to replace with a queue.
    row, col, val = sorted_list.pop(0)
    rowStart = [row]
    cols = [col]
    vals = [val]
    # This does not get returned. Used to keep track.
    rows = [row]
    for i, row in enumerate(sorted_list):
      # need to check for empty rows and resolve them.
      if row[0] > rows[-1]:
        rowStart.append(i + 1)
      cols.append(row[1])
      vals.append(row[2])
      rows.append(row[0])
    # Add sentinel value.
    rowStart.append(len(vals))
    return rowStart, cols, vals

  def __repr__(self):
    return '\n'.join([str(row) for row in self.to_dense_matrix()])

  def to_dense_matrix(self):
    """Returns a dense matrix corresponding to this sparse matrix."""
    dense_mat = [[0 for column in range (self.columns)]
                 for row in range(self.rows)]
    print(self.rowStart)
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
   
