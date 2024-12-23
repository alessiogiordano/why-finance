#!/bin/sh

#
#  setup.sh
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

clear

echo "WhyFinance"
echo "Progetto di Distributed Systems and Big Data"
echo "Anno Accademico 2024-25"
echo "(C) 2024 Luca Montera, Alessio Giordano"
echo "---"

if [[ " $@ " =~ " -h " || " $@ " =~ " --help " ]]; then
    printf "%s\n" "USAGE: ./setup.sh [--install-protobuf-suppport] [--build-protos] [--reset] [-h]"
    printf "%s\t%s\n" "--install-protobuf-suppport " " Installs the proper version of grpcio(-tools)"
    printf "%s\t\t\t%s\n" "--build-protos " " Deletes ./Protos/.build and rebuilds ProtoBufs"
    printf "%s\t\t\t%s\n" "--rebuild " " Forces rebuild of images before running"
    printf "%s\t\t\t%s\n" "--reset " " Deletes built local images and volumes before running"
    printf "%s\t\t\t%s\n" "--hard-reset " " Deletes all built images and volumes before running"
    printf "%s\t\t\t%s\n" "--no-run " " Does not start the Docker Compose file"
    printf "%s\t\t\t%s\n" "-h, --help " " Prints this message"
    exit 0;
fi

cd "$(dirname "$0")" # Go to the root of the project

#
# Install ProtoBuf and gRPC support in the local Python environment
#
if [[ " $@ " =~ " --install-protobuf-support " ]]; then
    echo "Installing grpcio and grpcio-tools..."
    pip3 install grpcio==1.62.1 grpcio-tools==1.62.1
fi

#
# Build ProtoBufs if requested or necessary
#

if [[ ! -d "./Protos/.build" || " $@ " =~ " --build-protos " ]]; then
    printf "%s" "Building Protocol Buffers..."
    rm -rf "./Protos/.build"
    mkdir "./Protos/.build"
    cd "./Protos/"
    #
    for PROTO in ./*.proto; do
        python3 -m grpc_tools.protoc -I . --python_out=./.build/ --pyi_out=./.build/ --grpc_python_out=./.build/ "$PROTO"
    done
    #python3 -m grpc_tools.protoc -I ../. --python_out=. --pyi_out=. --grpc_python_out=. users.proto
    #python3 -m grpc_tools.protoc -I ../. --python_out=. --pyi_out=. --grpc_python_out=. stocks.proto
    #python3 -m grpc_tools.protoc -I ../. --python_out=. --pyi_out=. --grpc_python_out=. circuit_breaker.proto
    #python3 -m grpc_tools.protoc -I ../. --python_out=. --pyi_out=. http.proto
    #
    cd ..
    echo " Done"
fi

cd "./Containers/"

#
# Delete previous instances
#

if [[ " $@ " =~ " --reset " ]]; then
    printf "%s" "Deleting all local images and volumes..."
    docker compose down --rmi local -v
    echo " Done"
fi

if [[ " $@ " =~ " --hard-reset " ]]; then
    printf "%s" "Deleting all images and volumes..."
    docker compose down --rmi all -v
    echo " Done"
fi

#
# Start the system using the Docker Compose file
#

if [[ " $@ " =~ " --no-run " ]]; then
    exit 0;
fi

echo "Starting up the system..."
if [[ " $@ " =~ " --rebuild " ]]; then
    docker compose up --build --force-recreate --no-deps
else
    docker compose up
fi