#! /usr/bin/python3
"""End to end demonstration script for sparse_sor."""
import data_io
import vector
import sparse_sor
import sparse_matrix
from proto_genfiles.protos import sor_pb2
import sys

if __name__ == "__main__":
  # Remove one for the program itself.
  args = len(sys.argv) - 1
  print("Number of additional command line args passed: %s" % args)
  # Default values
  input_filename = "nas_Sor.in"
  output_filename = "nas_Sor.out"
  if args > 2:
    raise Exception("Error: Too many command line args passed")
  elif args == 2:
    output_filename = sys.argv[2]
  if args >= 1:
    input_filename = sys.argv[1]
  print("Reading input data from file: %s" % input_filename)
  matrix_proto, vector_proto = data_io.read_input(input_filename)
  matrix_a = sparse_matrix.SparseMatrix(matrix_proto)
  vector_b = vector.Vector(vector_proto=vector_proto)
  solver = sparse_sor.SparseSorSolver(matrix_a, vector_b, 10, .0001, 1.0)
  solution_proto = solver.to_proto()
  print("Calculation complete. Writing solution to: %s" % output_filename)
  data_io.write_output(solution_proto, output_filename)
