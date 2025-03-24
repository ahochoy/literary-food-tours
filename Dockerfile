# Use the official NiceGUI image as the base image
FROM amd64/python:3.13-slim

# Set working directory
WORKDIR /app

# Copy the application code to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy environment variable vault to the container
COPY .env.vault .

# Copy the application code to the container
COPY /app .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Set the default command to run the NiceGUI app
CMD ["python3", "main.py"]
