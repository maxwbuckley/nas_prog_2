"""Class and methods pertaining to Sparse Matrices."""
import validation 

class NonConformableException(Exception):
  """Exception for when tries to multiply non conformable matrices."""
  pass


class SparseMatrix(object):
  def __init__(self, sparse_matrix_proto):
    # Lots to do here.
    validation.ValidateSparseMatrixProto(sparse_matrix_proto)
    self.columns = sparse_matrix_proto.column_count
    self.rows = sparse_matrix_proto.row_count
    self.rowStart, self.cols, self.vals = self.getCsrStructure(sparse_matrix_proto.values)
  
  def getCsrStrucutre(sparse_value_protos):
    temp_list = []
    for value in sparse_value_protos:
      temp_list.apend((value.row_index, value.col_index, value.value))
    sorted_list = sorted(temp_list, key=lambda: (element[0], element[1]))
    row, col, val = sorted_list[0]
    rowStart = [row]
    cols = [col]
    vals = [val]
    for row in sorted_list:
      if row[0] > rowStart[-1]:
        rowStart.append(row[0])
      cols.append(row[1])
      vals.append(row[2])
    return rowStart, cols, vals
    

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
   
