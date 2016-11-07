#! /usr/bin/python3
"""Unit tests associated with io.py."""
from proto_genfiles.protos import sor_pb2
import unittest
import data_io

class IoTest(unittest.TestCase):

  def setUp(self):
    self.matrix_proto = sor_pb2.SparseMatrix(
        matrix_name="a", row_count=3, column_count=3)
    for i in range(0, 3):
      value = self.matrix_proto.values.add()
      value.row_index = i
      value.column_index = i
      value.value = (i + 1) * 3.9

    self.negative_matrix_proto = sor_pb2.SparseMatrix(
        matrix_name="a-", row_count=3, column_count=3)
    for i in range(0, 3):
      value = self.negative_matrix_proto.values.add()
      value.row_index = i
      value.column_index = i
      value.value = -(i + 1) * 2.1

    self.vector_proto = sor_pb2.Vector(
        vector_name="b", length=3)
    self.vector_proto.values.extend([1.0, 3.6, 9.1])

    self.negative_vector_proto = sor_pb2.Vector(
        vector_name="b-", length=3)
    self.negative_vector_proto.values.extend([-1.0, -3.6, -9.1])

  def testReadFile(self):
    # TODO(rob): Complete
    pass

  def testReadInput(self):
    filename = 'nas_Sor.in'
    file_contents = data_io._read_file(filename)
    a, b = data_io.read_input(filename)
    expected = str(a) + '\n' + str(b) + '\n'
    self.assertEqual(expected, file_contents)

  def testWriteOutput(self):
    # TODO(rob): Complete
    pass

  def testProcessStringMatrixProto(self):
    matrix_proto_a = data_io._process_string_matrix_proto(
        str(self.matrix_proto))
    self.assertEqual(matrix_proto_a, self.matrix_proto)

  def testProcessStringMatrixProto_NegativeValues(self):
    negative_matrix_proto = data_io._process_string_matrix_proto(
        str(self.negative_matrix_proto))
    self.assertEqual(negative_matrix_proto, self.negative_matrix_proto)

  def testProcessStringVectorProto(self):
    vector_proto_b = data_io._process_string_vector_proto(
        str(self.vector_proto))
    self.assertEqual(vector_proto_b, self.vector_proto)

  def testProcessStringVectorProto_NegativeValues(self):
    negative_vector_proto = data_io._process_string_vector_proto(
        str(self.negative_vector_proto))
    self.assertEqual(negative_vector_proto, self.negative_vector_proto)

if __name__ == '__main__':
  unittest.main()
