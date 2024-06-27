#!/bin/bash

CONTAINER_NAME="discord-bot-container"
IMAGE_NAME="discord-bot"

# Stop and remove the existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container..."
    docker rm -f $CONTAINER_NAME
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Start a new container
echo "Starting new container..."
docker run --env-file .env -d --name $CONTAINER_NAME $IMAGE_NAME

# Follow the logs of the new container
echo "Following logs..."
docker logs -f $CONTAINER_NAME
