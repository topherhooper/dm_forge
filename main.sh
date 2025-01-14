#!/bin/bash

# Build the Docker image
docker build -t flask-vtt .

# Run the Docker container
docker run -p 8080:8080 flask-vtt

# Determine the URL to access the webpage
if [ -n "$CODESPACE_NAME" ]; then
    # If running in a GitHub Codespace
    echo "The application is running. Access it at: https://${CODESPACE_NAME}-8080.githubpreview.dev"
else
    # If running locally
    echo "The application is running. Access it at: http://localhost:8080"
fi

# Documentation on how to build and run the Docker container
# To build the Docker image, run:
# docker build -t flask-vtt .
# To run the Docker container, run:
# docker run -p 8080:8080 flask-vtt
