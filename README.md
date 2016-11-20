# nas_prog_2

# Setup
Users will need to install protobuf-compiler v3.0 or greater in addtion to the
required python3 libraries.

When you run the following command at the command line:
`
protoc --version
`

You should see libprotoc 3.0.0 or greater.

Then from the root directory of the project you need to run:
`
protoc protos/sor.proto --python_out=proto_genfiles
`
To regenerate the proto genfiles into their folder from the proto files.

Running the current proto_example.py generates some example proto vectors and
  matrices.
```
./proto_example.py 

vector_name: "b"
length: 3
values: 3
values: 4
values: 5

matrix_name: "a"
row_count: 3
column_count: 3
values {
  value: 3.9
}
values {
  row_index: 1
  column_index: 1
  value: 7.8
}
values {
  row_index: 2
  column_index: 2
  value: 11.7
}

```
# Testing

To run all unit tests run the following from the nas_prog_2 directory.

```
python3 -m unittest discover -p '*_test.py'
```

# Running

To run the black scholes program run.

```
python3 black_scholes.py
```

To execute an example SOR program that reads the input file and writes the
output file.

```
python3 sparse_sor_demo.py
```
To run some experiments.

```
python3 experiment.py
```


