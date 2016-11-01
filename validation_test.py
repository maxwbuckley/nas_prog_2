#! /usr/bin/python3
"""Unit tests associated with validation.py."""
from proto_genfiles.protos import sor_pb2
import unittest
import validation

class ValidationTest(unittest.TestCase):
  def testValidateVectorProto_Success(self):
    vector = sor_pb2.Vector(vector_name="test", length=3)
    vector.values.extend([i for i in range(3, 6)])
    self.assertTrue(validation.ValidateVectorProto(vector))


  def testValidateVectorProto_InvalidLength(self):
    vector = sor_pb2.Vector(vector_name="test", length=12)
    vector.values.extend([i for i in range(3, 6)])
    self.assertRaises(
        validation.ValidationError, validation.ValidateVectorProto, vector)

  def testValidateSparseMatrixProto_Success(self):
    pass

  def testValidateSparseMatrixProto_OutOfBounds(self):
    pass

  def testValidateSparseMatrixProto_Collisions(self):
    pass

  def testValidateNumberList_Success(self):
    self.assertTrue(validation.ValidateNumberList([1, 2, 4, 6.5]))
  
  def testValidateNumberList_Failure(self):
    self.assertRaises(
        validation.ValidationError, validation.ValidateNumberList,
        ["Howdy", 2, 4, 6.5])

if __name__ == '__main__':
  unittest.main() 
