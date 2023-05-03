# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Load environment variables from .env file
RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Load environment variables from .env file
RUN apt-get purge -y --auto-remove gettext
RUN pip install python-dotenv

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Load environment variables from .env file
RUN python -m dotenv $(find /app -name ".env*")

# Run app.py when the container launches
CMD ["python", "summarize.py"]
