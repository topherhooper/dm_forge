#!/bin/bash

# Change to the transcriber directory
cd ./transcriber

# Build the Docker image
docker build -t transcriber .

# Run the Docker container
docker run --rm -v $(pwd):/app transcriber