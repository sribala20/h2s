# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /flask-api

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

ENV FLASK_APP=server.py

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your Flask app listens on
EXPOSE 5000

# Start the Flask app
CMD ["flask run"]