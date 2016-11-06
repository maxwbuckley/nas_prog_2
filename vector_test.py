#! /usr/bin/python3
"""Unit tests associated with validation.py."""
from proto_genfiles.protos import sor_pb2
import unittest
import vector

class VectorTest(unittest.TestCase):

  def testVector_FromProto(self):
    vector_a_proto = sor_pb2.Vector(vector_name = "a", length = 5,
                                    values = [1, 2, 3, 4, 5])        
    vector_a = vector.Vector(vector_proto=vector_a_proto)
                
    expected = vector.Vector(number_list=[1, 2, 3, 4, 5])
      
    self.assertEqual(expected.values, vector_a.values)
      
  def testVector_FromNumberList(self):
    expected = [1, 2, 3, 4, 5]
    vector_a = vector.Vector(number_list=expected)
    
    self.assertEqual(expected, vector_a.values)
      
  def testVector_WithZeroValues(self):
    expected = [0, 1, 2, 3, 4]
    vector_a = vector.Vector(number_list=expected)
    
    self.assertEqual(expected, vector_a.values)

if __name__ == '__main__':
  unittest.main()
