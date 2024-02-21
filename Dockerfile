#TO RUN: docker-compose up --build
#then go to http://localhost:9201/ to check elastic search is running
#and http://localhost:5001/ for website
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for pycryptodome
RUN apt-get update && apt-get install -y \
    build-essential \
    libgmp-dev \
    libmpc-dev \
    libmpfr-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
