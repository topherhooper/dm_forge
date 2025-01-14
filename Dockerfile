# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
	libgl1-mesa-glx \
	libglib2.0-0

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=app.py

COPY . /app

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

# Documentation on how to build and run the Docker container
# To build the Docker image, run:
# docker build -t flask-vtt .
# To run the Docker container, run:
# docker run -p 8080:8080 flask-vtt
