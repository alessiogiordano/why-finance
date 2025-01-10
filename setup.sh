#!/bin/sh

#
#  setup.sh
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/12/24.
#

clear

echo "WhyFinance"
echo "Progetto di Distributed Systems and Big Data"
echo "Anno Accademico 2024-25"
echo "(C) 2024 Luca Montera, Alessio Giordano"
echo "---"

if [[ " $@ " =~ " -h " || " $@ " =~ " --help " ]]; then
    printf "%s\n" "USAGE: ./setup.sh [-d | -k] [--install-protobuf-suppport] [--build-protos] [-h] ..."
    printf "%s\t%s\n" "--transfer-certificate aps.pem" " Copies the APNS certificate into the project"
    printf "%s\t%s\n" "--install-protobuf-suppport " " Installs the proper version of grpcio(-tools)"
    printf "%s\t\t\t%s\n" "--build-protos " " Deletes ./Protos/.build and rebuilds ProtoBufs"
    printf "%s\t\t\t%s\n" "--rebuild " " Forces rebuild of images before running"
    printf "%s\t\t\t%s\n" "--reset " " Deletes built local images and volumes before running"
    printf "%s\t\t\t%s\n" "--hard-reset " " Deletes all built images and volumes before running"
    printf "%s\t\t\t%s\n" "-d --docker " " Run Docker Compose through the Docker Engine"
    printf "%s\t\t\t%s\n" "-k --kind " " Run Kubernetes Cluster through Kind"
    printf "%s\t\t\t%s\n" "-h, --help " " Prints this message"
    exit 0;
fi

#
# Command Line Arguments
#

TRANSFER_CERTIFICATE=false
if [[ " $@ " =~ " --transfer-certificate " ]]; then
    TRANSFER_CERTIFICATE=true
fi
INSTALL_PROTOBUF_SUPPORT=false
if [[ " $@ " =~ " --install-protobuf-support " ]]; then
    INSTALL_PROTOBUF_SUPPORT=true
fi
BUILD_PROTOS=false
if [[ " $@ " =~ " --build-protos " ]]; then
    BUILD_PROTOS=true
fi
REBUILD=false
if [[ " $@ " =~ " --rebuild " ]]; then
    REBUILD=true
fi
RESET=false
if [[ " $@ " =~ " --reset " ]]; then
    RESET=true
fi
HARD_RESET=false
if [[ " $@ " =~ " --hard-reset " ]]; then
    HARD_RESET=true
fi
NO_RUN=false
if [[ " $@ " =~ " --no-run " ]]; then
    NO_RUN=true
fi
RUN_DOCKER=false
if [[ " $@ " =~ " --docker " ]]; then
    RUN_DOCKER=true
fi
RUN_KIND=false
if [[ " $@ " =~ " --kind " ]]; then
    RUN_KIND=true
fi

if [[ "$RUN_DOCKER" = true && "$RUN_KIND" = true ]]; then
    echo "Only one execution method can be specified, either --docker or --kind"
    exit 1
fi

#
# Gather certificate path
#
CERTIFICATE=""
# arguments are iterated over to search for the certificate flag
while [[ "$#" -gt 1 ]]; do
    case "$1" in
        --transfer-certificate)
            shift
            DIRECTORY=$(dirname "$1" 2> /dev/null)
            FILENAME=$(basename "$1" 2> /dev/null)
            CERTIFICATE=$(cd "$DIRECTORY" && pwd 2> /dev/null)/"$FILENAME"
            break
            ;;
        *)  shift
            ;;
    esac
done
# if it is not a valid path, then it is discarded
if [[ ! -f "$CERTIFICATE" ]]; then
    CERTIFICATE=""
fi

#
# Change working directory
#
cd "$(dirname "$0")" # Go to the root of the project

#
# Transfer certificate 
#
if [[ ! -f "./Containers/NotificationCenter/aps.pem" || "$TRANSFER_CERTIFICATE" = true ]]; then
    if [[ -z "$CERTIFICATE" ]]; then
        echo "Provide a valid file path with --transfer-certificate to copy the APNS certificate over to the NotificationCenter microservice."
        exit 1;
    fi
    printf "%s" "Copying APNS certificate..."
    cp -f "$CERTIFICATE" "./Containers/NotificationCenter/aps.pem" > /dev/null 2>&1
    echo " Done"
fi

#
# Install ProtoBuf and gRPC support in the local Python environment
#
if [[ "$INSTALL_PROTOBUF_SUPPORT" = true ]]; then
    printf "%s" "Installing grpcio and grpcio-tools..."
    pip3 install grpcio==1.62.1 grpcio-tools==1.62.1 > /dev/null 2>&1
    echo " Done"
fi

#
# Build ProtoBufs if requested or necessary
#

if [[ ! -d "./Protos/.build" || "$BUILD_PROTOS" = true ]]; then
    printf "%s" "Building Protocol Buffers..."
    rm -rf "./Protos/.build" > /dev/null 2>&1
    mkdir "./Protos/.build" > /dev/null 2>&1
    cd "./Protos/" > /dev/null 2>&1
    #
    for PROTO in ./*.proto; do
        python3 -m grpc_tools.protoc -I . --python_out=./.build/ --pyi_out=./.build/ --grpc_python_out=./.build/ "$PROTO" > /dev/null 2>&1
    done
    #
    cd ..
    echo " Done"
fi

cd "./Containers/"

#
# Delete previous instances
#

if [[ "$RESET" = true ]]; then
    printf "%s" "Deleting all Docker Compose local images and volumes..."
    docker compose down --rmi local -v > /dev/null 2>&1
    printf "%s" " Kind cluster..."
    kind delete cluster --name why-finance > /dev/null 2>&1
    echo " Done"
fi

if [[ "$HARD_RESET" = true ]]; then
    printf "%s" "Deleting all Docker Compose images and volumes..."
    docker compose down --rmi all -v > /dev/null 2>&1
    printf "%s" " Kind cluster..."
    kind delete cluster --name why-finance > /dev/null 2>&1
    cd ..
    printf "%s" " Built images..."
    for DIRECTORY in ./Containers/*/; do
        TAG=$(basename "$DIRECTORY" | awk '{print tolower($0)}')
        if [[ -f "${DIRECTORY}tag.txt" ]]; then
            TAG=$(cat "${DIRECTORY}tag.txt")
        fi
        docker rmi -f "${TAG}:latest" > /dev/null 2>&1
    done
    cd "./Containers/"
    echo " Done"
fi

#
# Start the system using the Docker Compose file
#

if [[ "$RUN_DOCKER" = true ]]; then
    echo "Starting up the system using Docker..."
    if [[ "$REBUILD" = true ]]; then
        docker compose up --build --force-recreate --no-deps
    else
        docker compose up
    fi
fi

#
# Start the system using Kind
#

if [[ "$RUN_KIND" = true ]]; then
    echo "Starting up the system using Kind..."
    kind create cluster --config kind-config.yaml --name why-finance
    kubectl create configmap why-finance-env --from-env-file=.env --context kind-why-finance --namespace why-finance
    cd ..
    for DIRECTORY in ./Containers/*/; do
        TAG=$(basename "$DIRECTORY" | awk '{print tolower($0)}')
        if [[ -f "${DIRECTORY}tag.txt" ]]; then
            TAG=$(cat "${DIRECTORY}tag.txt")
        fi
        if [[ -f "${DIRECTORY}Dockerfile" ]]; then
            echo "Building ${TAG}:latest..."
            docker build -t "${TAG}:latest" -f "${DIRECTORY}Dockerfile" .
            printf "%s" "Loading ${TAG}:latest... "
            kind load docker-image "${TAG}:latest" --name why-finance
        fi
        if [[ -f "${DIRECTORY}manifest.yaml" ]]; then
            printf "%s" "Applying $(basename "$DIRECTORY")/manifest.yaml... "
            kubectl apply -f "${DIRECTORY}manifest.yaml" --context kind-why-finance
        fi
    done
    echo "Done starting up the system"
fi