# nas_prog_2

# Setup
Users will need to install protobuf-compiler v3.0 or greater in addtion to the required python3 libraries. #TODO: Put in links

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
