#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 up | down"
    exit 1
}

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    usage
fi

case $1 in
    up)
    # Scale up 5 replicas
    echo "Scaling up to 5 replicas..."
    docker-compose up --scale app=5 -d
    ;;

    down)
    # Scale down to 3 replica
    echo "Scaling down to 3 replica..."
    docker-compose up --scale app=3 -d
    ;;

  *)
    # Invalid command - show help message
    usage
    ;;
esac
