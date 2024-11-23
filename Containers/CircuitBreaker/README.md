# Circuit Breaker
## Install dependencies
pip3 install grpcio==1.62.1 grpcio-tools==1.62.1
pip3 install -r requirements.txt
## How-to compile related protocol buffers
python3 -m grpc_tools.protoc -I ../../Protos/. --python_out=. --pyi_out=. --grpc_python_out=. circuit_breaker.proto
python3 -m grpc_tools.protoc -I ../../Protos/. --python_out=. --pyi_out=. http.proto
