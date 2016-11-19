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
    # Add validation
    self.columns = len(dense_matrix[0])
    self.rows = len(dense_matrix)
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
      A list of tuples of the form row index, col_index, value.
    """
    tuple_list = []
    for i in range(len(dense_matrix)):
      for j in range(len(dense_matrix[0])):
        if dense_matrix[i][j] != 0:
          tuple_list.append((i, j, dense_matrix[i][j]))
    return tuple_list

  def _convert_proto_to_tuple_list(self, sparse_value_proto):
    """Convert a proto into a list of its non 0 valued tuples.

    Args:
      sparse_value_proto: sor_pb2.SparseMatrix proto.
    Returns:
      A list of tuples of the form row index, col_index, value.
    """
    tuple_list = []
    for value in sparse_value_proto:
      tuple_list.append((value.row_index, value.column_index, value.value))
    return tuple_list

  def _get_csr_structure(self, sparse_value_proto=None, dense_matrix=None):
    """Convert either a proto or a dense matrix into csr format

    Args:
      sparse_value_proto: sor_pb2.SparseMatrix proto.
      dense_matrix: A list of lists with only numerical entries.
    Returns:
      Three lists; the rowstart, column and values in the matrix
    """
    # Need some checking
    if sparse_value_proto is not None:
      temp_list = self._convert_proto_to_tuple_list(sparse_value_proto)
    elif dense_matrix is not None:
      temp_list = self._convert_dense_matrix_to_tuple_list(dense_matrix)
    sorted_list = sorted(temp_list, key=lambda element: (element[0], element[1]))
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
        for _ in range(row[0] - rows[-1]):
          # This is to account for potentially empty rows.
          rowStart.append(i + 1)
      cols.append(row[1])
      vals.append(row[2])
      rows.append(row[0])
    # Add sentinel value.
    rowStart.append(len(vals))
    return rowStart, cols, vals

  def __repr__(self):
    """Change print format to print csr in dense form."""
    return '\n'.join([str(row) for row in self.to_dense_matrix()])

  def to_dense_matrix(self):
    """Returns a dense matrix corresponding to this sparse matrix."""
    dense_mat = [[0 for column in range (self.columns)]
                 for row in range(self.rows)]
    for i in range(self.rows):
      for j in range(self.rowStart[i], self.rowStart[i + 1]):
        dense_mat[i][self.cols[j]] = self.vals[j]
    return dense_mat

  def is_square_matrix(self):
    """Checks whether matrix is square.
    Returns:
      Boolean of whether or not it is square.
    """
    return self.columns == self.rows


  def is_strictly_row_diagonally_dominant(self):
    """Checks whether matrix is diagonally dominant.

    Returns:
      Boolean of whether or not it is diagonally dominant.
    """
    if not self.is_square_matrix():
      # All diagonally dominant matrices are square
      return False
    dense_mat = self.to_dense_matrix()
    for i in range(len(dense_mat)):
      abs_row_sum = 0
      for j in range(len(dense_mat[i])):
          if i != j:
            abs_row_sum += abs(dense_mat[i][j])
      if abs(dense_mat[i][i]) <= abs_row_sum:
        return False
    return True

  def multiply_by_vector(self, vector_object):
    """Multiply this matrix by the target vector

      Args:
        vector_object: A vector.Vector object.i

      Returns:
        a list of numbers.

      Raises:
        NonConformableException if the matrix and vector are non
            conformable.
    """
    if not isinstance(vector_object, vector.Vector):
      raise Exception("Can only multiply by a vector")
    if not self.is_conformable(vector_object):
      raise NonConformableException("")
    # New empty 0 vector
    new_vec = [0] * self.rows
    for i in range(self.rows):
      for j in range(self.rowStart[i], self.rowStart[i + 1]):
          new_vec[i] += self.vals[j] * vector_object.values[self.cols[j]]
    return new_vec

  def is_conformable(self, vector_object):
    """Returns a boolean if the two matrices are conformable.

    Args:
      vector: a vector.Vector object.

    Returns:
      boolean if this Matrix and that vector are conformable.
    Raises:
      NonConformableException if the dimensions don't match.
    """
    if self.columns == vector_object.length:
      return True
    return False

  def one_norm(self):
    """Returns the matrix one norm. The maximum column sum."""
    one_norm = 0
    col_totals = {}
    for i, col in enumerate(self.cols):
      new_total = col_totals.get(col, 0) + abs(self.vals[i])
      col_totals[col] = new_total
      if new_total > one_norm:
        one_norm = new_total
    return one_norm

  def infinity_norm(self):
    """Returns the matrix infinity norm. The maximum row sum."""
    infinity_norm = 0
    for i in range(self.rows):
      row_sum = 0
      for j in range(self.rowStart[i], self.rowStart[i + 1]):
        row_sum += abs(self.vals[j])
      if row_sum > infinity_norm:
        infinity_norm = row_sum
    return infinity_norm

