# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system libraries required by OpenCV
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install any needed packages specified in Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches using Pipenv
CMD ["pipenv", "run", "python", "app.py"]
