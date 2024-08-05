#!/bin/bash

# Build the Docker image
docker build -t flask-video-chat-app .

# Run the Docker container
docker run -p 8080:8080 flask-video-chat-app &

# Determine the URL to access the webpage
if [ -n "$CODESPACE_NAME" ]; then
    # If running in a GitHub Codespace
    echo "The application is running. Access it at: https://${CODESPACE_NAME}-8080.githubpreview.dev"
else
    # If running locally
    echo "The application is running. Access it at: http://localhost:8080"
fi