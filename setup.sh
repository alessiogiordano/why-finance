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
set +o posix 2> /dev/null # Enable <() expression

PWD=$(pwd)
WHYFINANCE_PATH=$(dirname "$(realpath $0)")
cd "$WHYFINANCE_PATH"

ARGS=$(echo " $@ ") # Solves syntax error when using ash and providing more than one argument
                    # if expr "$ARGS" : ".* -h .*" > /dev/null; then
                    # if [[ "$ARGS" =~ " -h " ]]; then
echo "WhyFinance"
echo "Progetto di Distributed Systems and Big Data"
echo "Anno Accademico 2024-25"
echo "(C) 2024-2025 Luca Montera, Alessio Giordano"
echo "---"

if [[ "$ARGS" =~ " -h " || "$ARGS" =~ " --help " ]]; then
    printf "%s\n" "USAGE: ./setup.sh [-d | -k] [--install-protobuf-suppport] [--build-protos] [-h] ..."
    printf "%s\t%s\n" "--transfer-certificate aps.pem" " Copies the APNS certificate into the project"
    printf "%s\t%s\n" "--install-protobuf-suppport " " Installs the proper version of grpcio(-tools)"
    printf "%s\t\t\t%s\n" "--build-protos " " Deletes ./Protos/.build and rebuilds ProtoBufs"
    printf "%s\t\t\t%s\n" "--rebuild " " Forces rebuild of images before running"
    printf "%s\t\t\t%s\n" "--reset " " Deletes built local images and volumes before running"
    printf "%s\t\t\t%s\n" "--hard-reset " " Deletes all built images and volumes before running"
    printf "%s\t\t\t%s\n" "-d --docker " " Run Docker Compose through the Docker Engine"
    printf "%s\t\t\t%s\n" "-k --kind " " Run Kubernetes Cluster through Kind"
    printf "%s\t\t\t%s\n" "--log-pods " " Log status of Kubernetes nodes to ./log.txt"
    printf "%s\t\t\t%s\n" "-h, --help " " Prints this message"
    cd "$PWD"
    exit 0
fi

#
# Command Line Arguments
#

TRANSFER_CERTIFICATE=false
if [[ "$ARGS" =~ " --transfer-certificate " ]]; then
    TRANSFER_CERTIFICATE=true
fi
INSTALL_PROTOBUF_SUPPORT=false
if [[ "$ARGS" =~ " --install-protobuf-support " ]]; then
    INSTALL_PROTOBUF_SUPPORT=true
fi
BUILD_PROTOS=false
if [[ "$ARGS" =~ " --build-protos " ]]; then
    BUILD_PROTOS=true
fi
REBUILD=false
if [[ "$ARGS" =~ " --rebuild " ]]; then
    REBUILD=true
fi
RESET=false
if [[ "$ARGS" =~ " --reset " ]]; then
    RESET=true
fi
HARD_RESET=false
if [[ "$ARGS" =~ " --hard-reset " ]]; then
    HARD_RESET=true
fi
RUN_DOCKER=false
if [[ "$ARGS" =~ " -d " || "$ARGS" =~ " --docker " ]]; then
    RUN_DOCKER=true
fi
RUN_KIND=false
if [[ "$ARGS" =~ " -k " || "$ARGS" =~ " --kind " ]]; then
    RUN_KIND=true
fi
LOG_PODS=false
if [[ "$ARGS" =~ " --log-pods " ]]; then
    LOG_PODS=true
fi

if [[ "$RUN_DOCKER" = true && "$RUN_KIND" = true ]]; then
    echo "Only one execution method can be specified, either --docker or --kind"
    cd "$PWD"
    exit 1
fi

#
# Check dependencies
#

isavailable () {
    if [ ! -n "$(which $1)" ]; then
        echo "Missing dependency: $1"
        cd "$PWD"
        exit 1
    fi
}

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
        cd "$PWD"
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
    isavailable "pip3"
    printf "%s" "Installing grpcio and grpcio-tools..."
    pip3 install grpcio==1.62.1 grpcio-tools==1.62.1 > /dev/null 2>&1
    echo " Done"
fi

#
# Build ProtoBufs if requested or necessary
#

if [[ ! -d "./Protos/.build" || "$BUILD_PROTOS" = true ]]; then
    isavailable "python3"
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
    for COMMAND in "docker" "docker-compose" "kind"; do
        isavailable "$COMMAND"
    done
    printf "%s" "Deleting Kind cluster..."
    kind delete cluster --name why-finance > /dev/null 2>&1
    printf "%s" " Docker Compose images and volumes (local only)..."
    docker compose down --rmi local -v > /dev/null 2>&1
    echo " Done"
fi

if [[ "$HARD_RESET" = true ]]; then
    for COMMAND in "docker" "docker-compose" "kind"; do
        isavailable "$COMMAND"
    done
    printf "%s" "Deleting Kind cluster..."
    kind delete cluster --name why-finance > /dev/null 2>&1
    printf "%s" " Docker Compose images and volumes (all)..."
    docker compose down --rmi all -v > /dev/null 2>&1
    cd ..
    printf "%s" " Built images..."
    for DIRECTORY in ./Containers/*/; do
        TAG=$(basename "$DIRECTORY" | awk '{print tolower($0)}')
        if [[ -f "${DIRECTORY}tag.txt" ]]; then
            TAG=$(cat "${DIRECTORY}tag.txt")
        fi
        docker rmi -f "${TAG}:latest" > /dev/null 2>&1
    done
    printf "%s" " Build cache..."
    printf "y\n" | docker builder prune > /dev/null 2>&1
    cd "./Containers/"
    echo " Done"
fi

#
# Start the system using the Docker Compose file
#

if [[ "$RUN_DOCKER" = true ]]; then
    echo "Starting up the system using Docker..."
    for COMMAND in "docker" "docker-compose"; do
        isavailable "$COMMAND"
    done
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
    echo "Starting up the system using Kind... ($(date))"
    for COMMAND in "kind" "kubectl" "docker" "envsubst"; do
        isavailable "$COMMAND"
    done
    #
    # Check main memory and CPU
    #
    if [ -f /proc/meminfo ]; then
        MAIN_MEMORY=$(cat /proc/meminfo | grep MemTotal | awk '{print $2 * 1024}') # Bytes
        # Main memory should at least be 2 GB
        if [ "$MAIN_MEMORY" -lt "2400000000" ]; then
            printf "\e[31mRAM is less than 2.5GB, you will have trouble running the Kubernetes cluster\e[0m\n"
        fi
    fi
    if [ -n "$(which nproc)" ]; then
        CPU_COUNT=$(nproc --all)
        if [ "$CPU_COUNT" -lt "4" ]; then
            printf "\e[31mCPU should be at least quad core, you will have trouble running the Kubernetes cluster\e[0m\n"
        fi
    fi
    #
    # Environment variables
    #
    set -a # Automatically export all variables to child processes
    source .env
    #
    # Create cluster
    #
    rm ".manifest.yaml" 2> /dev/null
    WHYFINANCE_PATH="$WHYFINANCE_PATH" envsubst < "kind-config.yaml" > ".manifest.yaml"
    kind delete cluster --name why-finance > /dev/null 2>&1
    printf '%s' 'Creating cluster "why-finance"...'
    kind create cluster --config ".manifest.yaml" --name why-finance > /dev/null 2>&1
    echo " Done"
    echo "You can now use your cluster with: kubectl cluster-info --context kind-why-finance"
    rm ".manifest.yaml" 2> /dev/null
    kubectl create namespace why-finance
    kubectl create configmap why-finance-env --from-env-file=.env --context kind-why-finance --namespace why-finance
    #
    # Build Docker Images
    #
    cd .. # Return to root (required by Dockerfile context)
    # Get terminal lines and columns
    read -r LINES COLUMNS < <(stty size)
    for DIRECTORY in ./Containers/*/; do
        TAG=$(basename "$DIRECTORY" | awk '{print tolower($0)}')
        if [[ -f "${DIRECTORY}tag.txt" ]]; then
            TAG=$(cat "${DIRECTORY}tag.txt")
        fi
        if [[ -f "${DIRECTORY}Dockerfile" ]]; then
            printf "%s" "Building ${TAG}:latest... "
            if ! docker inspect --type=image "${TAG}:latest" > /dev/null 2>&1; then
                echo ""
                docker build --progress=plain -t "${TAG}:latest" -f "${DIRECTORY}Dockerfile" . 2>&1 | while IFS= read -r LINE; do
                    printf "\033[2K" # Clear line
                    if [ ! -z "$LINE" ]; then
                        NUM_LINES=$(echo $(( $(echo "$LINE" | wc -c) / COLUMNS )))
                        if [ "$NUM_LINES" -ne "0" ]; then
                            TRUNCATE_TO=$(( COLUMNS - 3 ))
                            OUTPUT="${LINE:0:TRUNCATE_TO}..."
                            printf "\e[2m\r%s\e[0m" "$OUTPUT" # Dim line that gets printed
                        else
                            printf "\e[2m\r%s\e[0m" "$LINE" # Dim line that gets printed
                        fi
                    else
                        printf "\r"
                    fi
                done
                printf "\r" # Go to beginning of line
                printf "\033[2K" # Clear line
                printf "\033[A" # Go to previous line
                printf "\033[2K" # Clear line
                #
                echo "Building ${TAG}:latest... Done"
            else
                echo "Image already exists"
            fi
        fi
    done
    #
    # Load Docker Images inside Kind
    #
    for DIRECTORY in ./Containers/*/; do
        TAG=$(basename "$DIRECTORY" | awk '{print tolower($0)}')
        if [[ -f "${DIRECTORY}tag.txt" ]]; then
            TAG=$(cat "${DIRECTORY}tag.txt")
        fi
        if [[ -f "${DIRECTORY}Dockerfile" ]]; then
            printf "%s" "Loading ${TAG}:latest..."
            kind load docker-image "${TAG}:latest" --name why-finance > /dev/null 2>&1
            echo " Done"
        fi
    done
    #
    # Apply Kubernetes Manifests
    #
    for DIRECTORY in ./Containers/*/; do
        TAG=$(basename "$DIRECTORY" | awk '{print tolower($0)}')
        if [[ -f "${DIRECTORY}tag.txt" ]]; then
            TAG=$(cat "${DIRECTORY}tag.txt")
        fi
        if [[ -f "${DIRECTORY}manifest.yaml" ]]; then
            printf "%s" "Applying $(basename "$DIRECTORY")/manifest.yaml..."
            rm ".manifest.yaml" 2> /dev/null
            WHYFINANCE_PATH="/why-finance" envsubst < "${DIRECTORY}manifest.yaml" > ".manifest.yaml"
            kubectl apply -f ".manifest.yaml" --context kind-why-finance > /dev/null 2>&1
            rm ".manifest.yaml" 2> /dev/null
            echo " Done"
        fi
    done
    echo "Done setting up pods ($(date))"
    if [[ "$LOG_PODS" = true ]]; then
        printf "%s" "Waiting for all pods to become ready..."
    else
        printf "%s" "Waiting for all pods to become ready (CTRL+C to skip)..."
    fi
    # Executed twice in case some pods are not immediately created and therefore not counted
    # Negative timeout of 60 minutes should be interpreted as timeout of a week according to docs
    kubectl wait pod --all --for=condition=Ready=true --timeout -60m --context kind-why-finance --namespace why-finance > /dev/null 2>&1
    kubectl wait pod --all --for=condition=Ready=true --timeout -60m --context kind-why-finance --namespace why-finance > /dev/null 2>&1
    printf "\a" # Visual and Audio Bell
    echo " Done starting up the system ($(date))"
    set +a
    cd "./Containers/"
fi

cd .. # Return to root

#
# Log Kubernetes Status
#

if [[ "$LOG_PODS" = true ]]; then
    isavailable "kubectl"
    echo "Gathering Pods..."
    PODS=$(kubectl get pod --context kind-why-finance --namespace why-finance --no-headers -o custom-columns=":metadata.name")
    printf "%s" "Logging"
    printf "%s" " Pods..."
    kubectl get pod --context kind-why-finance --namespace why-finance >> log.txt 2>&1
    for POD in $(kubectl get pod --context kind-why-finance --namespace why-finance --no-headers -o custom-columns=":metadata.name"); do
        printf "%s" " $POD..."
        kubectl describe pod "$POD" --context kind-why-finance --namespace why-finance >> log.txt 2>&1
        kubectl logs "$POD" --context kind-why-finance --namespace why-finance >> log.txt 2>&1
        echo "" >> log.txt
    done
    echo " Done"
fi

cd "$PWD" # Return to caller