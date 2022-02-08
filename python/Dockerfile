# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# Copy local code to the container image.
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Run the applications
CMD ["python", "main.py"]