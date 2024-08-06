# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the transcriber script into the container
COPY . /app

# Set the default command to run the transcriber script
CMD ["python", "transcriber.py"]